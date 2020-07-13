
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: Urban Lab / Laboratorio de econometría espacial urbana - PAP4J05                           -- #
# -- script: wsgi.py : script para inicializar el dashboard                                              -- #
# -- author: FranciscoME / PAP4J05                                                                       -- #
# -- license: MIT                                                                                        -- #
# -- repository: https://github.com/IFFranciscoME/Urban_Lab_App                                          -- #
# -- --------------------------------------------------------------------------------------------------- -- #

from app.dash import app
from config import config


server = app.server
def main():
    app.run_server(debug=config.debug, host=config.host, port=config.port)


if __name__ == "__main__":
    main()

