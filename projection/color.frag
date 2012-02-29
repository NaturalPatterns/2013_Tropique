uniform sampler2D texture;
void main(void)
{
    vec2 p = gl_TexCoord[0].st;
    float c = texture2D(texture, p).r;
    gl_FragColor = (1.0-c)*gl_Color + c*vec4(0.0, 0.0, 1.0 - c, 1.0);
}
