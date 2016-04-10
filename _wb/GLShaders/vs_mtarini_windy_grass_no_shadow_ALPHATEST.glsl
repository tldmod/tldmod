uniform vec4 vMaterialColor;
uniform float fFogDensity;
uniform mat4 matWorldViewProj;
uniform mat4 matWorldView;
attribute vec3 inPosition;
attribute vec4 inColor0;
attribute vec2 inTexCoord;
varying vec4 Color;
varying vec2 Tex0;
varying float Fog;

uniform float time_var;

void main ()
{
   vec3 _wobbly_position = inPosition;

   float windAmount  = sin(time_var * 0.1014) + cos(time_var * 0.1413);
         windAmount *= windAmount;

   float t2 = time_var + dot(inPosition.xy, vec2(6.5, 4.5));
   float windPhase = sin(t2 * 3.9) * cos(t2 * 2.3);

  _wobbly_position += vec3(0.018) // *(vPosition.z+50.0)
				    * windPhase * (windAmount + 0.2)
                    * inColor0.w; // distance from ground stored in alpha channes with openbrf easteregg! ;)

  vec4 tmpvar_1;
  tmpvar_1.w = 1.0;
  tmpvar_1.xyz = inPosition;
  vec4 tmpvar_2;
  vec3 tmpvar_3;
  tmpvar_3 = (matWorldView * tmpvar_1).xyz;
  tmpvar_2.xyz = (inColor0.zyxw * vMaterialColor).xyz;
  float tmpvar_4;
  tmpvar_4 = sqrt(dot (tmpvar_3, tmpvar_3));
  tmpvar_2.w = min (1.0, ((1.0 -
    (tmpvar_4 / 50.0)
  ) * 2.0));
  gl_Position = (matWorldViewProj * tmpvar_1);
  Fog = (1.0/(exp2((tmpvar_4 * fFogDensity))));
  Color = tmpvar_2;
  Tex0 = inTexCoord;
}

