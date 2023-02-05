#!/usr/bin/env python

import clize
import os
from pathlib import Path


class PermChecker:
    instances = {}
    def __init__(self, name, infinitive, preposition, checker_fn):
        self.name = name
        self.infinitive = infinitive
        self.preposition = preposition
        self.checker_fn = checker_fn
        PermChecker.instances[self.name] = self

    def run(self, path_to_check):
        return self.checker_fn(path_to_check)


def check_read_perms(path_to_check):
    return os.access(path_to_check, os.R_OK)


def check_write_perms(path_to_check):
    return os.access(path_to_check, os.W_OK)


def check_execute_perms(path_to_check):
    #TODO this seems to give unexpected results, investigate
    return os.access(path_to_check, os.X_OK)

def check_parents_chdir(path_to_check: Path):
    print('Checking that all directories above have execute permissions...')
    path_to_check = Path(path_to_check)
    ex_checker = PermChecker('parents_chdir', 'checking parents execute bits', 'on', check_execute_perms)
    checked_path_parts = []
    part_lacked_exbit = False
    for part in path_to_check.parts:
        checked_path_parts.append(part)
        path_seg_to_check = Path(*checked_path_parts)
        if not ex_checker.run(path_seg_to_check):
            print(f'A parent directory, {path_seg_to_check}, lacks execute permission.')
            part_lacked_exbit = True
    return not part_lacked_exbit



PermChecker('read', 'reading', 'from ', check_read_perms)
PermChecker('write', 'writing', 'to ', check_read_perms)
PermChecker('execute', 'executing', '', check_read_perms)    # FIXME does this also cover cd and ls?

def main(*, action:'a', path_to_check:'p'):
    checker = PermChecker.instances[action]
    print(f'So you want to {checker.name} {checker.preposition}{path_to_check} ?')
    abspath_to_check = Path(path_to_check).absolute()
    print(f'In absolute terms, that path is:\n{abspath_to_check}')
    if checker.run(path_to_check):
        print('Looks to me like you can. So stop whining.')
    else:
        print('Not allowed. Let us check why.')
        check_parents_chdir(path_to_check)



if __name__ == '__main__':
    clize.run(main)
