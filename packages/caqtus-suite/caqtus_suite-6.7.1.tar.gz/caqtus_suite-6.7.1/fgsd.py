from caqtus.extension import Experiment
from caqtus.session.sql import PostgreSQLConfig
from caqtus.session.sql._session_maker import SQLiteConfig


if __name__ == "__main__":
    experiment = Experiment()
    experiment.setup_default_extensions()

    experiment.configure_storage(SQLiteConfig("database.db"))

    experiment_1 = Experiment()
    experiment_1.setup_default_extensions()
    experiment_1.configure_storage(PostgreSQLConfig.from_file("config.yaml"))

    # with (
    #     experiment_1.storage_session() as source_session,
    #     experiment.storage_session() as target_session,
    # ):
    #
    #     copy_sequence(
    #         PureSequencePath(r"\sequence"),
    #         source_session,
    #         PureSequencePath(r"\sequence"),
    #         target_session,
    #     ).unwrap()
    experiment.launch_condetrol()
