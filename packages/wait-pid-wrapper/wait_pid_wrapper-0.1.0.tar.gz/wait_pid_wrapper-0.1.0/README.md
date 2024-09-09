# Wait PID Wrapper

## Introduction

Start a process and store the process identifier in a pid file (`wait-pid-wrapper-exec`).

The pid file then can be awaited until the process ends (`wait-pid-wrapper-waitpid`).

This is useful for running a normal process as a service using SystemD, preventing it from
running concurrently or running for infinity.

SystemD is capable of running processes as a service but it cannot gracefully timeout (AFAIK).

You can either set `KillSignal` to something harmless or `KillMode=none` but then SystemD doesn't timeout the process.

## Usage

The following SystemD unit starts a sleep process with the following behavior:

command                   | is sleep running? | behavior 
--------------------------|-------------------|-----------------------------------------------------------------------------
systemctl start mysleep   | no                | start sleep
systemctl start mysleep   | yes               | sleep is already running
systemctl stop mysleep    | no                | nothing happens, sleep is not running
systemctl stop mysleep    | yes               | wait until sleep has finished, allow timeout to forcefully stop the process

```
[Unit]
Description=My sleep

[Service]
Type=exec
ExecStart=waitpidwrapper-exec mysleep sleep 9999
ExecStop=waitpidwrapper-waitpid mysleep
```
