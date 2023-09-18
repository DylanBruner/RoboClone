import tkinter as tk
from tkinter import ttk
from ui.battle.battlefield import BattleField

class Robot:
    def __init__(self, robot_name: str, file_location: str):
        self.robot_name = robot_name
        self.file_location = file_location

class RobotPackage:
    def __init__(self, package_name: str, robots: list[Robot] = []):
        self.package_name = package_name
        self.robots: list[Robot] = robots
    
    def add_robot(self, robot_name: Robot) -> None:
        self.robots.append(robot_name)

    def __str__(self):
        return self.package_name

class BattleCreator:
    SELECTED_ROBOTS_ITEMS = []
    def __init__(self, root: tk.Tk = None):
        self.root = tk.Tk() if root is None else root
        self.root.title("New Battle")
        self.root.geometry("900x650")  # Set the default window size
        self.root.resizable(False, False)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.robots_package_data: list[RobotPackage] = None

        self.create_robots_tab()
        self.create_rules_tab()

        self.create_buttons()

    def create_robots_tab(self):
        self.last_selected_package = None
        robots_tab = ttk.Frame(self.notebook)
        self.notebook.add(robots_tab, text="Robots")

        # Create a LabelFrame for "Available Robots" with a border
        available_robots_frame = ttk.LabelFrame(robots_tab, text="Available Robots")
        available_robots_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.packages_list = tk.Listbox(available_robots_frame, selectmode=tk.SINGLE, exportselection=False)
        self.robots_list = tk.Listbox(available_robots_frame, selectmode=tk.SINGLE, exportselection=True)

        def show_package_contents(event):
            if self.packages_list.curselection() == (): return
            self.last_selected_package = self.packages_list.curselection()
            selected_package = self.packages_list.get(self.packages_list.curselection())
            self.robots_list.delete(0, tk.END)

            if self.robots_package_data is None: raise Exception("No robots package data loaded")
            for package in self.robots_package_data:
                if package.package_name == selected_package:
                    for robot in package.robots:
                        self.robots_list.insert(tk.END, robot.robot_name)

        self.packages_list.bind("<<ListboxSelect>>", show_package_contents)

        self.packages_list.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.robots_list.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        available_robots_frame.grid_rowconfigure(0, weight=1)
        available_robots_frame.grid_columnconfigure(0, weight=1)
        available_robots_frame.grid_columnconfigure(1, weight=1)

        # Create buttons for adding and removing items
        buttons_frame = ttk.Frame(robots_tab)
        buttons_frame.grid(row=0, column=1, padx=0, pady=0, sticky="nsew")

        add_button = ttk.Button(buttons_frame, text="Add ->", command=self.add_item)
        add_all_button = ttk.Button(buttons_frame, text="Add All ->", command=self.add_all_items)
        remove_button = ttk.Button(buttons_frame, text="<- Remove", command=self.remove_item)
        remove_all_button = ttk.Button(buttons_frame, text="<- Remove All", command=self.remove_all_items)

        add_button.grid(row=0, column=0, padx=5, pady=(37, 0), sticky="nsew")
        add_all_button.grid(row=1, column=0, padx=5, pady=0, sticky="nsew")
        remove_button.grid(row=2, column=0, padx=5, pady=(402, 0), sticky="nsew")
        remove_all_button.grid(row=3, column=0, padx=5, pady=(0, 0), sticky="nsew")

        # Create a LabelFrame for "Selected Robots" with a border
        selected_robots_frame = ttk.LabelFrame(robots_tab, text="Selected Robots")
        selected_robots_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

        self.selected_robots_list = tk.Listbox(selected_robots_frame, selectmode=tk.SINGLE, exportselection=True)
        self.selected_robots_list.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")


        selected_robots_frame.grid_rowconfigure(0, weight=1)
        selected_robots_frame.grid_columnconfigure(0, weight=1)

        # Bind a double-click event to the robots_list to add selected item to selected_robots_list
        def add_selected_robot(event):
            selected_index = self.robots_list.curselection()
            if selected_index:
                selected_item = self.robots_list.get(selected_index[0])
                self.selected_robots_list.insert(tk.END, selected_item)

        self.robots_list.bind("<Double-Button-1>", add_selected_robot)

        # Modify the add_item method to add the selected item from robots_list to selected_robots_list
        def add_item(self):
            selected_index = self.robots_list.curselection()
            if selected_index:
                selected_item = self.robots_list.get(selected_index[0])
                self.selected_robots_list.insert(tk.END, selected_item)

        self.add_item = add_item  # Update the method

        # Bind a double-click event to the selected_robots_list to remove the selected item
        def remove_selected_robot(event):
            selected_index = self.selected_robots_list.curselection()
            if selected_index:
                self.selected_robots_list.delete(selected_index)

        self.selected_robots_list.bind("<Double-Button-1>", remove_selected_robot)

        # Configure row and column weights to make elements resize with the window
        robots_tab.grid_rowconfigure(0, weight=1)
        robots_tab.grid_columnconfigure(0, weight=1)
        robots_tab.grid_columnconfigure(1, weight=0)  # Set weight to 0 to prevent buttons from resizing vertically
        robots_tab.grid_columnconfigure(2, weight=1)

    def create_rules_tab(self):
        rules_tab = ttk.Frame(self.notebook)
        self.notebook.add(rules_tab, text="Rules")

        rules_tab.grid_rowconfigure(0, weight=1)
        rules_tab.grid_columnconfigure(0, weight=1)

    def create_buttons(self):
        button_frame = ttk.Frame(self.root)
        button_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        start_battle_button = ttk.Button(button_frame, text="Start Battle", command=self.start_battle)
        cancel_button = ttk.Button(button_frame, text="Cancel", command=self.root.destroy)

        #ttl width = 902, button width = 72
        start_battle_button.grid(row=0, column=1, padx=5, pady=(5, ), sticky="nsew")
        cancel_button.grid(row=0, column=0, padx=(((902 - 72 * 2) / 2) - 18, 1), pady=5, sticky="nsew")

    def add_item(self):
        if self.robots_list.curselection() == (): return
        self.selected_robots_list.insert(tk.END, self.robots_list.get(self.robots_list.curselection()))
        

    def add_all_items(self):
        if self.robots_list.size() < 0: return
        for i in range(self.robots_list.size()):
            self.selected_robots_list.insert(tk.END, self.robots_list.get(i))

    def remove_item(self):
        if self.selected_robots_list.curselection() == (): return
        self.selected_robots_list.delete(self.selected_robots_list.curselection())

    def remove_all_items(self):
        if self.selected_robots_list.size() < 0: return
        self.selected_robots_list.delete(0, tk.END)

    def start_battle(self):
        robots: list[Robot] = []
        for i in range(self.selected_robots_list.size()):
            for package in self.robots_package_data:
                for robot in package.robots:
                    if robot.robot_name == self.selected_robots_list.get(i):
                        robots.append(robot)
                        break
        
        # add all selected robots to SELECTED_ROBOTS_ITEMS
        BattleCreator.SELECTED_ROBOTS_ITEMS = []
        for robot in self.selected_robots_list.get(0, tk.END):
            BattleCreator.SELECTED_ROBOTS_ITEMS.append(robot)
            
        BattleField.setupNewBattle(robots)
        self.root.destroy()

    def populate_robot_data(self, data: list[RobotPackage]) -> None:
        self.robots_package_data = data
        for package in data:
            self.packages_list.insert(tk.END, package)
        for item in BattleCreator.SELECTED_ROBOTS_ITEMS:
            self.selected_robots_list.insert(tk.END, item)


if __name__ == "__main__":
    app = BattleCreator()
    app.populate_robot_data([
        RobotPackage("Package 1", [Robot("Robot 1", "file1"), Robot("Robot 2", "file2")]),
        RobotPackage("Package 2", [Robot("Robot 3", "file3"), Robot("Robot 4", "file4")]),
        RobotPackage("Package 3", [Robot("Robot 5", "file5"), Robot("Robot 6", "file6")]),
    ])
    app.root.mainloop()