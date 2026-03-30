import matplotlib.pyplot as plt
import uuid
import os

def generate_graph(values):

    folder = "static/graphs"

    # create folder if not exists
    os.makedirs(folder, exist_ok=True)

    filename = str(uuid.uuid4()) + ".png"

    path = os.path.join(folder, filename)

    plt.figure()

    plt.bar(range(len(values)), values)

    plt.xlabel("Features")
    plt.ylabel("Values")
    plt.title("Patient Feature Graph")

    plt.savefig(path)

    plt.close()

    # IMPORTANT: return path for HTML
    return "/static/graphs/" + filename