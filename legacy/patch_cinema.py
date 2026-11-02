p = 'index.html'
t = open(p, encoding='utf-8').read()

def rep(old, new):
    global t
    assert old in t, 'MISS: ' + old[:70]
    t = t.replace(old, new, 1)

# 1) imports
rep("import * as THREE from 'https://unpkg.com/three@0.160.0/build/three.module.js';",
"""import * as THREE from 'https://unpkg.com/three@0.160.0/build/three.module.js';
import { EffectComposer } from 'https://unpkg.com/three@0.160.0/examples/jsm/postprocessing/EffectComposer.js';
import { RenderPass } from 'https://unpkg.com/three@0.160.0/examples/jsm/postprocessing/RenderPass.js';
import { UnrealBloomPass } from 'https://unpkg.com/three@0.160.0/examples/jsm/postprocessing/UnrealBloomPass.js';
import { ShaderPass } from 'https://unpkg.com/three@0.160.0/examples/jsm/postprocessing/ShaderPass.js';
import { OutputPass } from 'https://unpkg.com/three@0.160.0/examples/jsm/postprocessing/OutputPass.js';
import { VignetteShader } from 'https://unpkg.com/three@0.160.0/examples/jsm/shaders/VignetteShader.js';
import Lenis from 'https://unpkg.com/lenis@1.3.27/dist/lenis.mjs';""")

# 2) composer after silk added
rep("  silk.frustumCulled = false;\n  scene.add(silk);",
"""  silk.frustumCulled = false;
  scene.add(silk);

  /* cinema postprocessing: bloom + chromatic aberration + vignette */
  const composer = new EffectComposer(renderer);
  composer.addPass(new RenderPass(scene, camera));
  const bloom = new UnrealBloomPass(new THREE.Vector2(innerWidth, innerHeight), IS_MOB ? .3 : .55, .5, .5);
  composer.addPass(bloom);
  const chromaShader = {
uniforms: { tDiffuse: { value: null }, uChroma: { value: IS_MOB ? .0009 : .0012 } },
vertexShader: `varying vec2 vUv; void main(){ vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.); }`,
fragmentShader: `uniform sampler2D tDiffuse; uniform float uChroma; varying vec2 vUv;
void main(){
vec2 dir = vUv - .5;
vec3 c;
c.r = texture2D(tDiffuse, vUv + dir * uChroma).r;
c.g = texture2D(tDiffuse, vUv).g;
c.b = texture2D(tDiffuse, vUv - dir * uChroma).b;
gl_FragColor = vec4(c, 1.);
}`
};
  const chromaPass = new ShaderPass(chromaShader);
  composer.addPass(chromaPass);
  const vigPass = new ShaderPass(VignetteShader);
  vigPass.uniforms.offset.value = .92;
  vigPass.uniforms.darkness.value = 1.15;
  composer.addPass(vigPass);
  composer.addPass(new OutputPass());

  /* buttery smooth scroll */
  const lenis = new Lenis({ lerp: .09, smoothWheel: true, touchMultiplier: 1.4 });
  let lastScroll01 = 0;""")

# 3) resize: composer too
rep("    renderer.setSize(innerWidth, innerHeight);\n    camera.aspect = innerWidth/innerHeight;",
"    renderer.setSize(innerWidth, innerHeight);\n    composer.setSize(innerWidth, innerHeight);\n    camera.aspect = innerWidth/innerHeight;")

# 4) camera choreography + velocity chroma + lenis raf
rep("    camera.lookAt(0, 8.5 - scroll01*10, 0);",
"""    camera.position.z = 30 - scroll01*5;
    camera.lookAt(0, 8.5 - scroll01*10, 0);
    camera.rotation.z += Math.sin(scroll01*6.28318)*.035;
    const vel = Math.abs(scroll01 - lastScroll01);
    lastScroll01 += (scroll01 - lastScroll01) * .2;
    chromaPass.uniforms.uChroma.value += ((IS_MOB ? .0008 : .0012) + vel*.02 - chromaPass.uniforms.uChroma.value) * .1;
    lenis.raf(performance.now());""")

# 5) composer render
rep("    renderer.render(scene, camera);", "    composer.render();")

# 6) fallback lenis when WebGL fails
rep("  onScroll();\n  tick();\n}",
"""  onScroll();
  tick();
} else {
/* fallback: buttery scroll even without WebGL */
const lenis = new Lenis({ lerp: .09, smoothWheel: true });
function rafLoop(time){ lenis.raf(time); requestAnimationFrame(rafLoop); }
requestAnimationFrame(rafLoop);
}""")

open(p, 'w', encoding='utf-8').write(t)
print('script ok, size:', len(t))
