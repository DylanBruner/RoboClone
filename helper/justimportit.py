import inspect, sys, os
import importlib.util

"""
Bypass circular import error
"""
class JustImportIt:
    marks: dict[str, list[str]] = {} # <filename, import statements>

    NORMAL = 0 # Mark and fix later
    DIRTY  = 1 # Attempt to import the class from the file directly by reading it's code (no dependancy resolution)
    UNSAFE = 2 # Attempt to import the class from the file directly by reading it's code (automatic dependancy resolution)
    ULTRA_UNSAFE = 3 # Recursive-automatic dependancy resolution

    @classmethod
    def resolve(self, mode: int = 0, deps: list[tuple[str, str]] or str = None) -> None:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        if exc_type is not ImportError: return

        calling_frame = inspect.currentframe().f_back
        import_statement = inspect.getsourcelines(calling_frame)[0][exc_traceback.tb_lineno - 1].strip().replace("try:","").strip()
        filename = exc_value.path.split("\\")[-1]

        if mode == self.NORMAL:    
            self.marks.setdefault(filename, [])
            self.marks[filename].append(import_statement)
        
        elif mode == self.DIRTY or mode == self.UNSAFE:
            if import_statement.startswith('from'):
                package = import_statement.split(" ")[1]
                things = [thing.replace(" ","") for thing in import_statement.split(" import ")[1].split(",")] 
            else:
                raise ValueError("This import statement is not supported with dirty mode yet")
            
            target = importlib.util.find_spec(package).origin
            results = {}
            for thing in things:
                try:
                    # results.append(self.getClass(package, thing))
                    results[thing] = JustImportIt.getClass(package, thing, deps)
                except Exception as e:
                    if mode == self.DIRTY:
                        raise e
                    elif mode == self.UNSAFE:
                        results[thing] = self.autoResolver(package, thing, runMode=mode)
            
            # get the caller's globals
            if any([result is None for result in results.values()]):
                raise ImportError(f"Failed to import {things} from {target}, (do not trust this!!!)")
            caller_globs = inspect.currentframe().f_back.f_globals
            caller_globs.update(results)

    @classmethod
    def fix(self) -> None:
        caller_filename = inspect.currentframe().f_back.f_code.co_filename.split("\\")[-1]
        caller_globs = inspect.currentframe().f_back.f_globals

        for statement in self.marks.get(caller_filename, []):
            exec(statement, caller_globs)
    
    @staticmethod
    def autoResolver(package: str, classname: str, runMode: int, max_tries: int = 10) -> object or None:
        deps: dict[str, object] = {}
        for i in range(max_tries):
            # attempt to import the class
            try:
                result = JustImportIt.getClass(package=package, class_name=classname, string_mode=True)
                locs = dict(deps)
                exec(result, locs, locs)
                return locs.get(classname, None)
            except NameError as e:
                missing = str(e).split("'")[1]
                if runMode == JustImportIt.UNSAFE:
                    results = JustImportIt.scanForClass(missing)
                    if len(results) == 0:
                        return None
                    else:
                        for file in results:
                            _class = JustImportIt.getClass(file.replace("\\",".").replace(".py","").lstrip("."), missing, [], False)
                            if _class is None: continue
                            deps[missing] = _class
                            break

            except Exception as e:
                ...

    @staticmethod
    def scanForClass(classname: str) -> list[str]:
        #returns all clases that have the same name
        # recursively scan all files in the current directory using os.walk
        results = []
        for root, dirs, files in os.walk("."):
            for file in files:
                if file.endswith(".py"):
                    with open(os.path.join(root, file), "r") as f:
                        code = f.readlines()
                    for line in code:
                        if "class" + classname + "(" in line.strip().replace(" ","") or "class" + classname + ":" in line.strip().replace(" ",""):
                            results.append(os.path.join(root, file))
                            break
        return list(set(results))

    @staticmethod
    def getClass(package: str, class_name: str, deps: list[tuple[str, str]] = None, string_mode: bool = False) -> object:
        deps = deps or []
        try:
            deps = [dep.split("::") if not isinstance(dep, tuple) else dep for dep in deps]
        except Exception as e:
            raise ValueError("Malformed dependancy list, use package::class_name or (package, class_name)")

        target = importlib.util.find_spec(package).origin
        with open(target, "r") as f:
            code: str = f.readlines()
        
        class_start = -1
        for i, line in enumerate(code):
            if line.strip().startswith("class") and class_name in line:
                class_start = i
                break
        if class_start == -1:
            return None
        
        class_end = -1
        for line in code[class_start + 1:]:
            if line.lstrip() == line and not (line.lstrip().startswith("\"") or line.lstrip().startswith("#")):
                class_end = code.index(line) - 1
                break
        else: class_end = len(code) # this *hopefully* means we reached the end of the file
        
        class_code: str = "".join(code[class_start:class_end])
        deps_code: list[str] = []

        for dependancy in deps:
            code = JustImportIt.getClass(dependancy[0], dependancy[1], [], True)
            deps_code.append(code)
        
        class_code = "\n".join(deps_code) + class_code

        if string_mode: return class_code

        locs = {}
        try:
            exec(class_code, {}, locs)
        except NameError as e:
            raise e
        return locs.get(class_name, None)