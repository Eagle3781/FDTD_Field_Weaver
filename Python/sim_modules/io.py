import json
import matplotlib.pyplot as plt

config_path = r"config/config.json"

# This module handles:
    # Data import and export
    # Graphing
    # Config file import

def configImport():
    with open(config_path) as conf:
        return json.loads(conf.read())

def exportEnvironment(environment):
    with open("./sim_out/environment.json", "w") as log:
        log.write(json.dumps(environment, indent=4))

def graph(out, environment, config):
    log_env = config["application_settings"]["log_environment_dict"]
    if log_env:
        exportEnvironment(environment)

    for i in config["graph_settings"]:
        graph_sing_pt = i["graph_single_point"]
        graph_surface = i["graph_surface"]

        if graph_surface & graph_sing_pt:
            graph_sing_pt = False
        
        if graph_sing_pt:
            point   = i["point_to_graph"]
            e_field = i["e_field"]

            if e_field:
                field_index = 0
            else:
                field_index = 1
            
            fig, ax = plt.subplots()
            y = []
            for i in out:
                y.append(i[field_index][point])

            if e_field:
                ax.set_xlabel("E Field Samples")
            else:
                ax.set_xlabel("H Field Samples")
            
            ax.set_title(f"Point in Space: {point}")
            ax.set_ylabel("Amplitude")
            ax.plot(y)
            plt.show()
        
        elif graph_surface:
            pass

