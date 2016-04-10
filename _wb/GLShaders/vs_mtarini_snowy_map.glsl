/* tld glsl shader -- vs_mtarini_snowy_map -- by swyter */

#version 120

attribute vec3 inPosition;
attribute vec3 inNormal;
attribute vec4 inColor0;
attribute vec4 inColor1;
attribute vec2 inTexCoord;

uniform mat4 matWorldViewProj;
uniform mat4 matWorldView;
uniform mat4 matWorld;

uniform vec4 vMaterialColor;
uniform vec4 vAmbientColor;
uniform vec4 vCameraPos;
uniform vec4 vSkyLightDir;
uniform vec4 vSunColor;
uniform vec4 vSunDir;

varying vec4 outColor0;
varying vec2 outTexCoord;
varying float outFog;
varying vec4 outSpec0;
varying vec4 outSunLight0;

#define MAP_SPECIAL_SNOW true

void main()
{
    gl_Position = matWorldViewProj * vec4(inPosition, 1.0);
	vec4 vWorldPos = matWorld * vec4(inPosition, 1.0);
    vec3 vWorldN = normalize(mat3(matWorld) * inNormal); //normal in world space

	outColor0 = inColor0.bgra * vMaterialColor;
	outTexCoord = inTexCoord;
	outFog = 1.f;

    float wNdotSun = max(0.0f, dot(vWorldN, -vSunDir.xyz));
	outSunLight0 = wNdotSun * vSunColor * vMaterialColor * inColor0;


    if (MAP_SPECIAL_SNOW)
    {
        // store altitude in Spec.x
        outSpec0.x = inPosition.z;

        // computation of specular
        vec3 vHalf = normalize(normalize(vCameraPos.xyz - vWorldPos.xyz) - vSkyLightDir.xyz);
        float fSpecular = pow(clamp( dot( vHalf, inNormal ), 0.0, 1.0), 32.0);
        outSpec0.y = fSpecular * vAmbientColor.x * 0.8; // store specular in SunLight.x
    }

}

