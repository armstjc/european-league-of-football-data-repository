from glob import glob
import os


def parse_names(name: str):
    name = name.replace('ß', 'ss')
    name = name.replace('Ã³', 'ss')
    name = name.replace('ó', 'o')
    name = name.replace('á', 'a')
    name = name.replace('é', 'e')
    name = name.replace('GroÃ³n', 'Grosse')
    name = name.replace('GrÃ³decki', 'Grodecki')
    name = name.replace('AdriÃ¡n', 'Adrian')
    name = name.replace('JimÃ©nez', 'Jimenez')
    name = name.replace('UÄ°nan', 'Ugur')
    name = name.replace('İ', 'I')
    name = name.replace('BerÃ§in', 'Bercin')
    name = name.replace('FernÃ¡ndez', 'Fernandez')
    # name = name.replace('GÃ¼ndoÄ§kesen', 'Agackesen')
    name = name.replace('GroÃ°nan', 'Grosse')
    # name = name.replace('ó', 'o')
    # name = name.replace('ó', 'o')

    return name


def parse_position_names(position: str) -> str:
    match position:
        case "Quarterback":
            return "QB"
        case "Running Back":
            return "RB"
        case "Halfback":
            return "HB"
        case "Fullback":
            return "FB"
        case "Wide Receiver":
            return "WR"
        case "Tight End":
            return "TE"
        case "Offensive Tackle":
            return "OT"
        case "Offensive Guard":
            return "OG"
        case "Center":
            return "C"
        case "Defensive Line":
            return "DL"
        case "Defensive End":
            return "DE"
        case "Defensive Tackle":
            return "DT"
        case "Linebacker":
            return "LB"
        case "Outside Linebacker":
            return "OLB"
        case "Inside Linebacker":
            return "ILB"
        case "Middle Linebacker":
            return "MLB"
        case "Cornerback":
            return "CB"
        case "Safety":
            return "SAF"
        case "Free Safety":
            return "FS"
        case "Strong Safety":
            return "SS"
        case "Kicker":
            return "K"
        case "Punter":
            return "P"
        case "Long Snapper":
            return "LS"
        case "PR":
            return "PR"
        case "KR":
            return "KR"
        case "OTHERS":
            return "ATH"
        case default:
            raise ValueError(f'Unhandled player position:\n\t{position}')


def reformat_folder_string(folder: str):
    """
    Reformats a string that represents a directory,
    into a string Python recognizes as a directory.

    Args:
        folder (str):
            Required parameter. Indicates the string you want
            to represent a directory, or a directory path.

    Returns:
        reform_folder (str):
            String intended to represent a directory, 
            or a directory path.
    """
    reform_folder = folder.replace("\\", "/")
    # print(f'Working Directory: \n\t{reform_folder}')
    return reform_folder


def get_json_in_folder(folder_path="") -> list:
    if len(folder_path) > 0:
        json_dir = folder_path
        del folder_path
    else:
        json_dir = "./raw_game_data/json/"
        del folder_path

    json_dir = os.path.abspath(json_dir)
    json_dir = reformat_folder_string(json_dir)
    print(json_dir)
    json_files = []
    json_file_list = glob(f"{json_dir}/*.json")

    for j in json_file_list:
        json_file = reformat_folder_string(j)

        json_files.append(json_file)
        del json_file

    return json_files
