from caqtus.extension import Experiment
from caqtus.session.sql import PostgreSQLConfig

if __name__ == "__main__":
    experiment = Experiment()
    experiment.setup_default_extensions()

    experiment.configure_storage(PostgreSQLConfig.from_file("config.yaml"))

    experiment.launch_condetrol()
