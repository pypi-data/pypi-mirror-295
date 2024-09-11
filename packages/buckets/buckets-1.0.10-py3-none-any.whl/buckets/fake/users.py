import numpy as np

def generate_user_id(max_users: int):
    """
    Generates a user_id based on a Pareto distribution.
    80% of the rows will be assigned to 20% of the users.

    Returns:
    int: A user_id.
    """
    # Pareto distribution parameters
    shape, mode = 1.16, 1

    # Generate a random number from the Pareto distribution
    pareto_num = (np.random.pareto(shape) + 1) * mode

    # Scale the number to the range of user_ids
    user_id = int(pareto_num * max_users / (mode + shape))

    # Ensure the user_id is within the valid range
    user_id = np.clip(user_id, 1, max_users)

    return user_id


def generate_user_id_normal(max_users: int):
    """
    Generates a user_id based on a normal distribution.
    The majority of the user_ids will be around the mean.

    Returns:
    int: A user_id.
    """
    # Normal distribution parameters
    #mean, std_dev = 0, 0.1
    mean, std_dev = 0, 0.15

    while True: 
        # Generate a random number from the normal distribution
        normal_num = np.random.normal(mean, std_dev) + 0.5

        # Ensure the user_id is within the valid range
        user_id = int(normal_num * max_users)
        
        if 1 <= user_id <= max_users:
            return user_id        


def get_user_name(user_id: int):
    # return the same name for a user_id
    
    popular_names = [
        "Liam",
        "Noah",
        "Oliver",
        "Elijah",
        "James",
        "William",
        "Benjamin",
        "Lucas",
        "Henry",
        "Alexander",
        "Mason",
        "Michael",
        "Ethan",
        "Daniel",
        "Jacob",
        "Logan",
        "Jackson",
        "Sebastian",
        "Aiden",
        "Matthew",
        "Samuel",
        "David",
        "Joseph",
        "Carter",
        "Owen",
        "Wyatt",
        "John",
        "Jack",
        "Luke",
        "Jayden",
        "Dylan",
        "Grayson",
        "Levi",
        "Isaac",
        "Gabriel",
        "Julian",
        "Mateo",
        "Anthony",
        "Jaxon",
        "Lincoln",
        "Joshua",
        "Christopher",
        "Andrew",
        "Theodore",
        "Caleb",
        "Ryan",
        "Asher",
        "Nathan",
        "Thomas",
        "Leo",
        "Isaiah",
        "Charles",
        "Josiah",
        "Hudson",
        "Christian",
        "Hunter",
        "Connor",
        "Landon",
        "Eli",
        "Adrian",
        "Jonathan",
        "Nolan",
        "Jeremiah",
        "Easton",
        "Ezekiel",
        "Colton",
        "Silas",
        "Gavin",
        "Chase",
        "Zachary",
        "Ryder",
        "Diego",
        "Jax",
        "Emmett",
        "Kaden",
        "Riley",
        "Robert",
        "Tyler",
        "Austin",
        "Jordan",
        "Cooper",
        "Xavier",
        "Jesse",
        "Luca",
        "Max",
        "Vincent",
        "Zane",
        "Liam",
        "Maverick",
        "Sawyer",
        "Graham",
        "Jude",
        "Karter",
        "Kylan",
        "Ronan",
        "Tobias",
        "Wesley",
        "Kendrick",
        "Dante",
        "Khalil",
        "Kendall",
        "Rafael",
        "Quinn",
        "Santiago",
        "Kairo",
        "Kason",
        "Kellan",
        "Koa",
        "Kye"
    ]

    last_names = [
        "Smith",
        "Johnson",
        "Williams",
        "Jones",
        "Brown",
        "Davis",
        "Miller",
        "Wilson",
        "Moore",
        "Taylor",
        "Anderson",
        "Thomas",
        "Jackson",
        "White",
        "Harris",
        "Martin",
        "Thompson",
        "Garcia",
        "Martinez",
        "Robinson",
        "Clark",
        "Rodriguez",
        "Lewis",
        "Lee",
        "Walker",
        "Hall",
        "Allen",
        "Young",
        "Hernandez",
        "King",
        "Wright",
        "Lopez",
        "Hill",
        "Scott",
        "Green",
        "Adams",
        "Baker",
        "Gonzalez",
        "Nelson",
        "Carter",
        "Mitchell",
        "Perez",
        "Roberts",
        "Turner",
        "Phillips",
        "Campbell",
        "Parker",
        "Evans",
        "Edwards",
        "Collins",
        "Stewart",
        "Sanchez",
        "Morris",
        "Rogers",
        "Reed",
        "Cook",
        "Morgan",
        "Bell",
        "Murphy",
        "Bailey",
        "Rivera",
        "Cooper",
        "Richardson",
        "Cox",
        "Howard",
        "Ward",
        "Torres",
        "Peterson",
        "Gray",
        "Ramirez",
        "James",
        "Watson",
        "Brooks",
        "Kelly",
        "Sanders",
        "Price",
        "Bennett",
        "Wood",
        "Barnes",
        "Ross",
        "Henderson",
        "Coleman",
        "Jenkins",
        "Perry",
        "Powell",
        "Long",
        "Patterson",
        "Hughes",
        "Flores",
        "Washington",
        "Butler",
        "Simmons",
        "Foster",
        "Gonzales",
        "Bryant",
        "Alexander",
        "Russell",
        "Griffin",
        "Diaz",
        "Hayes"
    ]
    
    first_name = popular_names[ user_id % len(popular_names)]
    last_name = last_names[ user_id % len(last_names)]
    name_set = int(user_id / (len(popular_names) * len(last_names))) 
    
    if name_set == 0:
        return f"{first_name} {last_name}"
    else:
        return f"{first_name} {chr(name_set+64)}. {last_name}"
    