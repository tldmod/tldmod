/* tld glsl shader -- vs_mtarini_swampy_map -- by swyter */

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

#define MAP_SPECIAL_SNOW false
#define MAP_SPECIAL_SWAMP true
#define UV_DISTORT_YES true
#define MULT_UV 1.0

void main()
{
    gl_Position = matWorldViewProj * vec4(inPosition, 1.0);
    vec4 vWorldPos = matWorld * vec4(inPosition, 1.0);
    vec3 vWorldN = normalize(mat3(matWorld) * inNormal); //normal in world space

   if (UV_DISTORT_YES)
   {
        // break texture patterns
        vec2 text_distort  = inTexCoord;
             text_distort += vec2( 1.0, 1.0) * 0.09 * sin(2.6 * inTexCoord.x);
             text_distort += vec2(-1.5, 1.0) * 0.12 * sin(4.0 * inTexCoord.y);
             text_distort *= MULT_UV;

        outTexCoord = text_distort;
   }
   else
   {
        outTexCoord = inTexCoord;
   }

    outColor0 = inColor0.bgra * vMaterialColor;

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

    if (MAP_SPECIAL_SWAMP)
    {
        // computes wheter inside swamp
        vec2 dist = vWorldPos.xy - vec2(-35.0, -27.0);
        outSpec0.x = (dot(dist, dist) > 38.0 * 38.0) ? 0.0 : 1.0; // stores swamp as yes no
    }
}

