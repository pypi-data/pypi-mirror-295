#****************************************************************************
#* task_cmd.py
#*
#* Copyright 2023 Matthew Ballance and Contributors
#*
#* Licensed under the Apache License, Version 2.0 (the "License"); you may 
#* not use this file except in compliance with the License.  
#* You may obtain a copy of the License at:
#*
#*   http://www.apache.org/licenses/LICENSE-2.0
#*
#* Unless required by applicable law or agreed to in writing, software 
#* distributed under the License is distributed on an "AS IS" BASIS, 
#* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  
#* See the License for the specific language governing permissions and 
#* limitations under the License.
#*
#* Created on:
#*     Author: 
#*
#****************************************************************************
import subprocess
from typing import Dict, List
from .env import Env
from .env_action import EnvAction
from .task import Task

class TaskCmd(Task):

    def __init__(self, 
                 name : str,
                 cmd : List[str],
                 cwd : str = None,
                 env : List[EnvAction] = None):
        super().__init__(name)
        self.cmd = cmd
        self.cwd = None
        self.env = env
        pass

    async def run(self):
        env = Env()

        if self.env is not None:
            for e in self.env:
                e.apply(env)

        res = subprocess.run(
            self.cmd,
            env=env.env,
            cwd=self.cwd,
            stderr=subprocess.STDOUT
        )

        if res.returncode != 0:
            raise Exception("Command %s failed (%s)" % (
                str(self.cmd), str(e)))

