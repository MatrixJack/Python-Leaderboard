# -[ Custom Modules ]- #
import pyModules.interface
import pyModules.sqlStream
import pyModules.kernalReg

# -[ Variables ]- #
register = pyModules.kernalReg.newRegister()

# -[ GUI Configuration ]- #

# -[ Configuration ]- #
register.set("list_size", 25)

register.set("ldb_size", "?x?")
register.set("ldb_resizable", True)

register.set("ddb_a_delete", True)

register.set("ldb_font", "Helvetica")
register.set("adm_font", "Helvetica")

register.set("max_points", 1000)

register.set("ldb_width", 15)
register.set("ldb_relief", "groove")

# -[ Colors ]- #
register.set("ldb_background_color", "#696969")
register.set("ldb_label_color", "#696969")
register.set("ldb_text_color", "#C0C0C0")
register.set("ldb_title_text_color", "#FFFFFF")

register.set("adm_background_color", "#696969")
register.set("adm_label_color", "#696969")
register.set("adm_text_color", "#C0C0C0")
register.set("adm_title_text_color", "#FFFFFF")

register.set("teamVariables", {})

# -[ Buff ]- #
def run():
    # -[ Append custom modules ]- #
    register.set("sqlModule", pyModules.sqlStream)

    # -[ Append custom module nodes ]- #
    register.set("register", register)
    register.set("sqlStream", pyModules.sqlStream.createNewStream("gInfo.db", False))

    # -[ Preload teams ]- #
    sqlStreamer = register.get("sqlStream")
    sqlTeams = sqlStreamer.select("*")

    if sqlTeams != None:
        variables = register.get("teamVariables")

        for teamSQLValue in sqlTeams:
            teamName, teamPoints = teamSQLValue[1], teamSQLValue[2]

            variables[teamName] = int(teamPoints)

        if register.get("ddb_a_delete"): sqlStreamer.executeSQL(f"DELETE FROM {sqlStreamer.getHostTableName()}", False)

    # -[ Create interface ]- #
    register.set("interfaceClasses", pyModules.interface.createInterfaceClasses(register))

    # -[ Start interface ]- #
    register.get("interfaceClasses").startThreads()

# -[ Execute ]- #
run()

print("executed")