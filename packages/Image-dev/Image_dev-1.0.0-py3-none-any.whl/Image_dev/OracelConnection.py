import oracledb
import os 
from .ReadFile import read

def connectDB():
    # Get the directory where this script is located
        current_dir = os.path.dirname(os.path.abspath(__file__))
        instant_client_path = os.path.join(current_dir, 'instantclient')
        oracledb.init_oracle_client(lib_dir=instant_client_path)
        try:
            config= read(r"Config.txt")
        except:
            config_path = os.path.join(current_dir, 'Config.txt')
            config= read(config_path)
        username=config['username'][0]
        password=config['password'][0]
        host=config['host'][0]
        port=config['port'][0]
        sid=config['sid'][0]
        connection = oracledb.connect(user=username, password=password, host=host, port=port, sid=sid)
        print("DB connected Successfully")
        return connection