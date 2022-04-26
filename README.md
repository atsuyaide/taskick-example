# Taskick Example Application

Here we will create an application that, when a PNG image is saved to a specific folder, converts the image to PDF and saves it to the output folder.

The application works with the following algorithm.

1. Detects when a PNG file is saved in the `input` folder.
2. The saved file path is propagated to the conversion script, which converts the file to PDF.
3. The converted PDF is saved in the `output` folder.
4. The input folder is deleted periodically to keep it clean.

See [Taskick](https://github.com/atsuyaide/taskick.git) for usage.

## Structures

This repository consists of the following folders.

```text
├── LICENSE
├── README.md         # This file.
├── batch.yaml
├── config
│   ├── logging.conf  # Can be specified by using the -l option.
│   ├── logging.yaml  # Can be specified by using the -l option.
│   ├── main.yaml     # Configuration file to main processing.
│   └── welcome.yaml  # Configuration file to display Welcome message at startup.
├── input             # When a PNG image is saved here, png2pdf.py is executed.
├── output            # Converted PDF is saved in this folder.
├── requirements.txt
└── src
    └── png2pdf.py    # Script to convert PNG to PDF.
```

Tusk and each file share functions and responsibilities as follows.

> 1. Detects when a PNG file is saved in the `input` folder. <- Taskick(Set main.yaml)
> 2. The saved file path is propagated to the conversion script, which converts the file to PDF. <- Taskick(Execute png2pdf.py)
> 3. The converted PDF is saved in the `output` folder. <- png2pdf.py
> 4. The input folder is deleted periodically to keep it clean. <- Taskick(rm -f input/*.*)

The detailed settings are configured in the following YAML(`welcome.yaml` and `main.yaml`) file.

welcome.yaml
```yaml
Welcome_taskick: # Task name
  status: 1 # Task status
  commands:
    - "echo $(date) Welcome to Taskick!"
    - "&&"
    - "echo waiting 5 seconds..."
    - "&&"
    - "sleep 5"
  execution:
    event_type: null # If event_type is NULL, it is executed only at startup.

```

main.yaml
```yaml
remove_files_in_input_folder:
  status: 1
  commands:
    - "rm -f input/*"
  execution:
    startup: true # If true, it is executed at startup.
    await_task:
      - "Welcome_taskick" # Set this task to run after the "Welcome_taskick" has finished running.
    event_type: "time"
    detail:
      when: "*/1 * * * *" # Crontab format: Run every 1 minute.

png2pdf:
  status: 1
  commands:
    - "python"
    - "./src/png2pdf.py"
  execution:
    startup: false
    event_type: "file"
    propagate: true # If true, events that occur at runtime (such as the path of an edited file) are passed to the running script.
    detail:
      path: "./input"
      recursive: false
      handler: # Support all watchdog.events.*EventHandler.
        name: "PatternMatchingEventHandler"
        args: # This args is passed to the handler.
          patterns:
            - "*.png"
      when: # Support created, deleted, modified, closed, moved event.
        - "created"
```

## Appendix

The execution interval and the criteria for starting can be changed by simply editing the `main.yaml` file.

For example,

- If you want a 5 minute interval to clean the `input` folder .

```yaml
when: "*/1 * * * *"
```

↓

```yaml
when: "*/5 * * * *"
```

- If you want to convert not only PNG but also JPEG files.

```yaml
patterns:
  - "*.png"
```

↓

```yaml
patterns:
  - "*.png"
  - "*.jpeg"
