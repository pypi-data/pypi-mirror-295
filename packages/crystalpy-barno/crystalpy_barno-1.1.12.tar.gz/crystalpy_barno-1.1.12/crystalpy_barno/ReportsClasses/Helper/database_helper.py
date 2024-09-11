# database_helper.py
# from crystalpy_barno.ReportsClasses.Base_Report import  *

# database_helper.py
class DatabaseConnectionHelper:
    _server_name = None
    _database_name = None
    _user_id = None
    _password = None

    @classmethod
    def get_database_name(cls):
        return cls._database_name

    @classmethod
    def set_connection_details(cls, server_name, database_name, user_id, password):
        """
        Set the database connection details.
        :param server_name: The server name for the database
        :param database_name: The database name
        :param user_id: The user ID for database login
        :param password: The password for database login
        """
        cls._server_name = server_name
        cls._database_name = database_name
        cls._user_id = user_id
        cls._password = password

    @classmethod
    def apply_connection(cls, crpt):
        """
        Apply the stored connection details to the provided report document.
        :param crpt: The report document object
        """
        if not all([cls._server_name, cls._database_name, cls._user_id, cls._password]):
            raise ValueError("Database connection details have not been set.")
        
        for mytable in crpt.Database.Tables:
            mylogin = mytable.LogOnInfo
            mylogin.ConnectionInfo.ServerName = cls._server_name
            mylogin.ConnectionInfo.DatabaseName = cls._database_name
            mylogin.ConnectionInfo.UserID = cls._user_id
            mylogin.ConnectionInfo.Password = cls._password
            mytable.ApplyLogOnInfo(mylogin)

