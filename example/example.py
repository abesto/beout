#!/usr/bin/env python -u

from functools import partial
import time
from termcolor import colored
from beout.terminal import writer

blue_bold = partial(colored, color='blue', attrs=['bold'])
green_bold = partial(colored, color='green', attrs=['bold'])
bold = partial(colored, attrs=['bold'])
green = partial(colored, color='green')

project = blue_bold('presentationservice')

writer.box(bold('Preparing for the installation of ') + project + bold(' on Docker LDE'))

writer.msg('Updating LDE tools')

with writer.scroll_lines(3) as scroll:
    for line in "Lorem xxxxxxxxxxxxxxxxxxxxx xxxxxxxxxxxxxx xxxxxxxxxxxxxxxxxxxxxxxxx xxxxxxxxxxxxxxxxxxxxx xxxxxxxxxxxxxxxxxxxxx xxxxxxxxxxxxxxxxxxxxx xxxxxxxxxxxxxxxxxxxxxxx xxxxxxxxxxxxxxxxx xxxxxxxxxxx ipsum dolor sit amet, consectetur adipiscing elit. Donec a diam lectus. Sed sit amet ipsum mauris. Maecenas congue ligula ac quam viverra nec consectetur ante hendrerit. Donec et mollis dolor. Praesent et diam eget libero egestas mattis sit amet vitae augue. Nam tincidunt congue enim, ut porta lorem lacinia consectetur. Donec ut libero sed arcu vehicula ultricies a non tortor. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean ut gravida lorem. Ut turpis felis, pulvinar a semper sed, adipiscing id dolor".split(". "):
        time.sleep(1)
        scroll(line)

writer.msg('Checking out ' + project + ' from git')
writer.progress_dot_every_n_seconds(1)
time.sleep(6)

writer.msg('Checking pre-requisites')
writer.substeps(3)
writer.msg(bold('python') + ' installation is ' + green('healthy'))
writer.msg(bold('java') + ' installation is ' + green('healthy'))
writer.msg(bold('docker') + ' installation is ' + green('healthy'))

writer.box(bold('All pre-requisites met, starting installation'))

writer.msg('Creating empty virtualenv')
writer.progress_dot_every_n_seconds(1)
time.sleep(2)

writer.msg('Adding LDE shared secret to overrides.cfg')

writer.msg('Preparing Docker image for ' + project)

writer.substeps(2)

writer.msg('Preparing Docker environment')
writer.progress_dot_every_n_seconds(1)
time.sleep(3)

writer.eta('Building Docker image and installing Python dependencies', 60 * 8)
time.sleep(5)

writer.eta('Installing Python dependencies into the local virtualenv', 4)
time.sleep(12)

writer.msg('Adding Dockerized ' + project + ' to LDE')
writer.msg('Disabling old, non-Dockerized ' + project + ' in LDE')

writer.box(bold('Installation finished, running basic health-checks'))

writer.msg('Starting ' + project + ' in Docker')
writer.progress_dot_every_n_seconds(1)
time.sleep(3)

writer.msg('Shared secret ' + green('matches') + ' the shared secret in authservice')
writer.msg('Sending GET to /healthcheck/')
writer.progress_dot_every_n_seconds(1)
time.sleep(3)
writer.msg('GET /healthcheck/ returned ' + green('200'))

writer.box(bold('Installation ') + green_bold('successfully') + bold(' finished'))

writer.done()
