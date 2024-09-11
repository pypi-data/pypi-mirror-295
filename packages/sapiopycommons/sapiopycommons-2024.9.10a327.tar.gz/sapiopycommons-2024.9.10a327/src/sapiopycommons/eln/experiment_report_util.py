from sapiopylib.rest.User import SapioUser
from sapiopylib.rest.pojo.datatype.FieldDefinition import FieldType
from sapiopylib.rest.utils.recordmodel.RecordModelWrapper import WrappedType

from sapiopycommons.customreport.custom_report_builder import CustomReportBuilder
from sapiopycommons.customreport.term_builder import TermBuilder
from sapiopycommons.general.aliases import SapioRecord, UserIdentifier, AliasUtil
from sapiopycommons.general.custom_report_util import CustomReportUtil
from sapiopycommons.recordmodel.record_handler import RecordHandler

_NOTEBOOK_ID = "EXPERIMENTID"
_RECORD_ID = "RECORDID"


# FR-46908 - Provide a utility class that holds experiment related custom reports e.g. getting all the experiments
# that given records were used in or getting all records of a datatype used in given experiments.
class ExperimentReportUtil:
    @staticmethod
    def map_records_to_experiment_ids(context: UserIdentifier, records: list[SapioRecord]) \
            -> dict[SapioRecord, list[int]]:
        """
        Return a dictionary mapping each record to a list of ids of experiments that they were used in.
        If a record wasn't used in any experiments then it will be mapped to an empty list.

        :param context: The current webhook context or a user object to send requests from.
        :param records: a list of records of the same data type.
        :return: a dictionary mapping each record to a list of ids of each experiment it was used in.
        """
        if not records:
            return {}

        user: SapioUser = AliasUtil.to_sapio_user(context)
        data_type_name: str = AliasUtil.to_singular_data_type_name(records)

        record_ids = [record.record_id for record in records]
        rows = ExperimentReportUtil.__get_record_experiment_relation_rows(user, data_type_name, record_ids=record_ids)

        id_to_record: dict[int, SapioRecord] = RecordHandler.map_by_id(records)
        record_to_exps: dict[SapioRecord, set[int]] = {record: set() for record in records}
        for row in rows:
            record_id: int = row[_RECORD_ID]
            exp_id: int = row[_NOTEBOOK_ID]
            record = id_to_record[record_id]
            record_to_exps[record].add(exp_id)

        return {record: list(exps) for record, exps in record_to_exps.items()}

    @staticmethod
    def map_experiments_to_records_of_type(context: UserIdentifier, exp_ids: list[int],
                                           wrapper_type: type[WrappedType]) -> dict[int, list[WrappedType]]:
        """
        Return a dictionary mapping each experiment id to a list of records of the given type that were used in each experiment.
        If an experiment didn't use any records of the given type then it will be mapped to an empty list.

        :param context: The current webhook context or a user object to send requests from.
        :param exp_ids: a list of experiment ids. These are specifically the Notebook Experiment ids which can be found in the title of the experiment.
        :param wrapper_type: The record model wrapper to use, corresponds to which data type we will query for.
        :return: a dictionary mapping each experiment id to a list of records of the given type that were used in that experiment.
        """
        if not exp_ids:
            return {}

        user = AliasUtil.to_sapio_user(context)
        record_handler = RecordHandler(user)
        data_type_name: str = wrapper_type.get_wrapper_data_type_name()

        rows = ExperimentReportUtil.__get_record_experiment_relation_rows(user, data_type_name, exp_ids=exp_ids)
        record_ids: set[int] = {row[_RECORD_ID] for row in rows}
        records = record_handler.query_models_by_id(wrapper_type, record_ids)

        id_to_record: dict[int, WrappedType] = RecordHandler.map_by_id(records)
        exp_to_records: dict[int, set[SapioRecord]] = {exp: set() for exp in exp_ids}
        for row in rows:
            record_id: int = row[_RECORD_ID]
            exp_id: int = row[_NOTEBOOK_ID]
            record = id_to_record[record_id]
            exp_to_records[exp_id].add(record)

        return {exp: list(records) for exp, records in exp_to_records.items()}

    @staticmethod
    def __get_record_experiment_relation_rows(user: SapioUser, data_type_name: str, record_ids: list[int] | None = None,
                                              exp_ids: list[int] | None = None) -> list[dict[str, int]]:
        """
        Return a list of dicts mapping \"RECORDID\" to the record id and \"EXPERIMENTID\" to the experiment id.
        At least one of record_ids and exp_ids should be provided.
        """
        assert (record_ids or exp_ids)

        if record_ids:
            records_term = TermBuilder.is_term(data_type_name, "RECORDID", record_ids)
        else:
            # Get all records of the given type
            records_term = TermBuilder.all_records_term(data_type_name)

        if exp_ids:
            exp_term = TermBuilder.is_term("NOTEBOOKEXPERIMENT", "EXPERIMENTID", exp_ids)
        else:
            # Get all experiments
            exp_term = TermBuilder.gte_term("NOTEBOOKEXPERIMENT", "EXPERIMENTID", "0")

        root_term = TermBuilder.and_terms(records_term, exp_term)

        # Join records on the experiment entry records that correspond to them.
        records_entry_join = TermBuilder.compare_is_term("EXPERIMENTENTRYRECORD", "RECORDID", data_type_name, "RECORDID")
        # Join entry records on the experiment entries they are in.
        experiment_entry_enb_entry_join = TermBuilder.compare_is_term("ENBENTRY", "ENTRYID", "EXPERIMENTENTRYRECORD", "ENTRYID")
        # Join entries on the experiments they are in.
        enb_entry_experiment_join = TermBuilder.compare_is_term("NOTEBOOKEXPERIMENT", "EXPERIMENTID", "ENBENTRY", "EXPERIMENTID")

        report_builder = CustomReportBuilder(data_type_name)
        report_builder.set_root_term(root_term)
        report_builder.add_column("RECORDID", FieldType.LONG, data_type=data_type_name)
        report_builder.add_column("EXPERIMENTID", FieldType.LONG, data_type="NOTEBOOKEXPERIMENT")
        report_builder.add_join(records_entry_join)
        report_builder.add_join(experiment_entry_enb_entry_join)
        report_builder.add_join(enb_entry_experiment_join)
        return CustomReportUtil.run_custom_report(user, report_builder.build_report_criteria())
