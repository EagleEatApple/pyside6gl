# import standard library

# import third party library

# import local library
from material.material import Material


class DepthMaterial(Material):

    def __init__(self):
        # vertex shader code
        vertexShaderCode = """
        in vec3 vertexPosition; 
        uniform mat4 projectionMatrix;
        uniform mat4 viewMatrix;
        uniform mat4 modelMatrix; 
        void main()
        {
            gl_Position = projectionMatrix * viewMatrix *
                          modelMatrix * vec4(vertexPosition, 1);
        }
        """

        # fragment shader code
        fragmentShaderCode = """
        out vec4 fragColor;
        void main()
        {
            float z = gl_FragCoord.z;
            fragColor = vec4(z, z, z, 1);
        }
        """
        # initialize shaders
        super().__init__(vertexShaderCode, fragmentShaderCode)
        self.locateUniforms()
