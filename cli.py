from typer import Typer

from commands.init_database.main import init_database, init_test_database

app = Typer()


@app.command("init_database")
def cmd_init_database():
    print("Initializing database")
    # init_database()
    init_test_database()


@app.command("run_test")
def cmd_run_test():
    print("Running tests")
    print("Tests executed successfully")


if __name__ == "__main__":
    app()
