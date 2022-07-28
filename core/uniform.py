# import standard library

# import third party library
from OpenGL.GL import *

# import local library


class Uniform(object):

    def __init__(self, dataType, data):

        # type of data
        #   int | bool | float | vec2 | vec3 | vec4 | mat4
        self.dataType = dataType

        # data to be sent to uniform variable
        self.data = data

        # reference for variable location in program
        self.variableRef = None

    # get and store reference for program variable with given name

    def locateVariable(self, programeRef, variableName):
        self.variableRef = glGetUniformLocation(programeRef, variableName)

    # store data in uniform variable previously located
    def uploadData(self):

        # if the program does not referencd the variable, then exit
        if self.variableRef == -1:
            return

        if self.dataType == "int":
            glUniform1i(self.variableRef, self.data)
        elif self.dataType == "bool":
            glUniform1i(self.variableRef, self.data)
        elif self.dataType == "float":
            glUniform1f(self.variableRef, self.data)
        elif self.dataType == "vec2":
            glUniform2f(self.variableRef, self.data[0], self.data[1])
        elif self.dataType == "vec3":
            glUniform3f(self.variableRef,
                        self.data[0], self.data[1], self.data[2])
        elif self.dataType == "vec4":
            glUniform4f(self.variableRef,
                        self.data[0], self.data[1], self.data[2], self.data[3])
        elif self.dataType == "mat4":
            glUniformMatrix4fv(self.variableRef, 1, GL_TRUE, self.data)
        else:
            raise Exception("Unknown Uniform data type: " + self.dataType)
