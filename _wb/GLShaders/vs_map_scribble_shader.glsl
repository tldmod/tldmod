/* tld glsl shader -- vs_map_scribble_shader -- by swyter */

attribute vec3 inPosition;
attribute vec3 inNormal;
attribute vec4 inColor0;
attribute vec4 inColor1;
attribute vec2 inTexCoord;

uniform mat4 matWorldViewProj;
uniform mat4 matWorldView;
uniform mat4 matWorld;

varying vec4 outColor0;
varying vec2 outTexCoord;
varying float outFog;

uniform vec4 vMaterialColor;

void main()
{
	gl_Position = matWorldViewProj * vec4(inPosition, 1.0);
	vec4 vWorldPos = matWorld * vec4(inPosition, 1.0);

	outColor0 = inColor0.bgra * vMaterialColor;
	outColor0.a *= clamp(normalize( vec3(matWorldView[2][0],matWorldView[2][1],matWorldView[2][2]) ).z * 2.0 - 1.0, 0.0, 1.0);

	outTexCoord = inTexCoord;
	outFog = 1.f;
}

