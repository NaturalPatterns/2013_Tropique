/* =========================================================================
   Reaction-diffusion vertex shader
   Copyright (C) 2008,2009,2010  Claude Heiland-Allen
   ========================================================================= */
void main()
{
    gl_FrontColor = gl_Color;
    gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
	gl_TexCoord[0] = gl_MultiTexCoord0;
}
