/* tld glsl shader -- vs_mtarini_windy_flora -- by swyter */

uniform vec4 vMaterialColor;
uniform vec4 vSunColor;
uniform vec4 vAmbientColor;
uniform float fFogDensity;

uniform mat4 matWorldViewProj;
uniform mat4 matWorldView;
uniform mat4 matWorld;

attribute vec3 inNormal;
attribute vec3 inPosition;
attribute vec4 inColor0;
attribute vec2 inTexCoord;

varying float Fog;
varying vec4 Color;
varying vec2 Tex0;
varying vec4 SunLight;
varying vec4 ShadowTexCoord;

uniform float time_var;

#define windSTR 0.18
#define UseUV true

void main ()
{
   vec3 _wobbly_position = inPosition;
   vec2 treePos = vec2(matWorld[0][3], matWorld[2][3]);

   float windAmount  = sin(time_var*0.1014) + cos(time_var*0.1413);
         windAmount *= windAmount;
         windAmount += 0.2;

   float t2 = time_var + dot(treePos, vec2(2.5,1.5)) + dot(inNormal, vec3(7.1,0.4,3.2));
   float windPhase = sin(t2*3.9)*cos(t2*2.3);

   if (UseUV)
   {
     _wobbly_position += inNormal * (inTexCoord.x-0.5) * (inTexCoord.y-0.5) * windPhase * windAmount * windSTR;
   }
   else
   {
	 _wobbly_position += inNormal * windPhase * windAmount * windSTR;
   }


  vec4 tmpvar_1;
  tmpvar_1.w = 1.0;
  tmpvar_1.xyz = _wobbly_position;
  vec4 tmpvar_2;
  vec4 tmpvar_3;
  vec4 tmpvar_4;
  tmpvar_4.w = 1.0;
  tmpvar_4.xyz = vSunColor.xyz;
  tmpvar_2 = (inColor0.zyxw * (vAmbientColor + (tmpvar_4 * 0.06)));
  tmpvar_2.w = (tmpvar_2.w * vMaterialColor.w);
  vec4 tmpvar_5;
  tmpvar_5.w = 1.0;
  tmpvar_5.xyz = vSunColor.xyz;
  vec3 tmpvar_6;
  tmpvar_6 = (matWorldView * tmpvar_1).xyz;
  gl_Position = (matWorldViewProj * tmpvar_1);
  Fog = (1.0/(exp2((
    sqrt(dot (tmpvar_6, tmpvar_6))
   * fFogDensity))));
  Color = tmpvar_2;
  Tex0 = inTexCoord;
  SunLight = ((tmpvar_5 * 0.34) * (vMaterialColor * inColor0.zyxw));
  ShadowTexCoord = tmpvar_3;
}

