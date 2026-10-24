import sys
import os
import json
import traceback


def extract_variables(namespace):
    variables = []
    for name, val in namespace.items():
        if name.startswith("__") or hasattr(val, "__file__"):
            continue

        type_name = type(val).__name__
        val_repr = repr(val)
        if len(val_repr) > 100:
            val_repr = val_repr[:97] + "..."

        variables.append({
            "name": name,
            "type": type_name,
            "value": val_repr
        })
    return variables


def main():
    if len(sys.argv) < 2:
        return

    # Check for --step flag
    step_mode = False
    args = sys.argv[1:]
    if "--step" in args:
        step_mode = True
        args.remove("--step")

    if not args:
        return

    script_path = os.path.abspath(args[0])

    user_globals = {
        "__name__": "__main__",
        "__file__": script_path,
        "__doc__": None,
    }

    try:
        with open(script_path, "r", encoding="utf-8") as f:
            code = compile(f.read(), script_path, "exec")

        if step_mode:
            def tracer(frame, event, arg):
                # Trace only inside the user's file
                if event == "line":
                    frame_file = os.path.abspath(frame.f_code.co_filename)
                    if frame_file == script_path:
                        lineno = frame.f_lineno
                        
                        # Merge globals and current function locals
                        combined = dict(user_globals)
                        combined.update(frame.f_locals)
                        vars_data = extract_variables(combined)

                        payload = json.dumps({"line": lineno, "vars": vars_data})
                        print(f"__WINNIE_STEP__:{payload}", flush=True)

                        # Block and wait for Step / Stop from Winnie
                        cmd = sys.stdin.readline().strip()
                        if cmd == "STOP":
                            sys.exit(0)
                        elif cmd == "CONTINUE":
                            sys.settrace(None)
                            return None
                return tracer

            sys.settrace(tracer)

        exec(code, user_globals)

    except SystemExit:
        pass
    except Exception:
        traceback.print_exc()
    finally:
        sys.settrace(None)
        final_vars = extract_variables(user_globals)
        json_data = json.dumps(final_vars)
        print(f"__WINNIE_VARS__:{json_data}", flush=True)


if __name__ == "__main__":
    main()
