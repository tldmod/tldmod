/* tld glsl shader -- vs_swy_simple_shader_spiritual -- by swyter */
#version 120

uniform vec4 vMaterialColor;
uniform float fFogDensity;

uniform mat4 matWorldViewProj;
uniform mat4 matWorldView;
uniform mat4 matWorld;

attribute vec3 inPosition;
attribute vec3 inNormal;
attribute vec4 inColor0;
attribute vec4 inColor1;
attribute vec2 inTexCoord;

varying vec4 outColor0;
varying vec2 outTexCoord;
varying float outFog;

uniform float time_var;

void main ()
{
  vec3 vPosition = inPosition;
  vec3 vNormal   = inNormal;
  vec4 vColor    = inColor0;
  
  gl_Position = (matWorldViewProj * vec4(vPosition, 1.0));

  vec4 vWorldPos =           (matWorld * vec4(vPosition, 1.0));
  vec3 vWorldN   = normalize((matWorld * vec4(vNormal,   1.0)).xyz);

  // red eye effect begin:
  vec3 vViewN = normalize((matWorldView * vec4(vNormal,  1.0)).xyz);

  vPosition.x += sin(vWorldPos.x + time_var*8.) / 50.;
  vPosition.z += cos(vWorldPos.x + time_var*8.) / 50.;

  vPosition.z += sin(vWorldPos.y + time_var*1.) / 50.;
  vPosition.y += cos(vWorldPos.x + time_var*2.) / 50.;


  vec3 P = (matWorldView * vec4(vPosition, 1.0)).xyz; //position in view space

  outTexCoord = inTexCoord;

  outColor0.rgb = (1.0 - abs(vViewN.zzz * 2.)) * 3.;//vColor * vMaterialColor;

  outColor0.rgb -= vColor.rgb;
  outColor0.a    = vWorldPos.y + 0.5;

  outFog = (1.0/(exp2(sqrt(dot (P, P)) * fFogDensity)));
}

