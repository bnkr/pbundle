import os
import subprocess
import re

class VirtualEnvironment(object):
    """Changing the virtualenvironment."""
    def __init__(self, path):
        self.path = path

    def create(self, python):
        subprocess.check_call(['virtualenv', "--python", python, self.path])

class PipInstaller(object):
    """Manages dependencies within a virtual environemnt.  It could be the case
    in the future that we have several kinds of managers but for now just
    pip."""
    def __init__(self, environment):
        self.pip = os.path.join(environment, "bin", "pip")

    def satisfy(self, requirements, upgrade=False):
        args = [self.pip, "install", ]
        if upgrade:
            args += ['-U']
        args += ["-r", requirements,]
        subprocess.check_call(args)

    def freeze(self, output):
        with open(output, "w") as io:
            subprocess.check_call([self.pip, "freeze",], stdout=io)

    def find_differences(self, lock):
        """Check for requirements that differ between the lock and the installed
        packages.  Requirements must be exact."""
        pipe = subprocess.Popen([self.pip, "freeze",], stdout=subprocess.PIPE)
        out, _ = pipe.communicate()
        pipe.wait()

        actual = out.split("\n")
        locked = open(lock).read().split("\n")
        return self._compare_requirements(actual, locked)

    def _compare_requirements(self, actual, locked):
        def nullify(line):
            line = line.strip()
            if not line:
                return None

            if re.match(r'\s+#', line):
                return None

            return line

        locked = filter(bool, map(nullify, locked))
        actual = filter(bool, map(nullify, actual))

        differences = {
            'missing': set(),
            'extra': set(),
            'inconsistent': []}

        for requirement in locked:
            if requirement not in actual:
                differences['missing'].add(requirement)

        for requirement in actual:
            if requirement not in locked:
                differences['extra'].add(requirement)

        return differences
