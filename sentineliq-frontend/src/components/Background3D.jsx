import { useRef } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { Points, PointMaterial } from '@react-three/drei';
import * as random from 'maath/random/dist/maath-random.esm';

function ParticleSphere() {
  const ref = useRef();
  // Generate spatial coordinates inside a 3D matrix sphere
  const sphere = random.inSphere(new Float32Array(1500), { radius: 1.5 });

  useFrame((state, delta) => {
    // Smoothly spin the particle spatial nodes over runtime execution ticks
    ref.current.rotation.x -= delta / 10;
    ref.current.rotation.y -= delta / 15;
  });

  return (
    <group rotation={[0, 0, Math.PI / 4]}>
      <Points ref={ref} positions={sphere} stride={3} frustumCulled={false}>
        <PointMaterial
          transparent
          color="#22d3ee" /* Cyan Neon Glow */
          size={0.015}
          sizeAttenuation={true}
          depthWrite={false}
        />
      </Points>
    </group>
  );
}

export default function Background3D() {
  return (
    <div className="fixed inset-0 -z-10 h-screen w-screen overflow-hidden bg-[#020617]">
      {/* Dynamic ambient glowing accent nodes using blur filters */}
      <div className="absolute top-1/4 left-1/4 h-96 w-96 rounded-full bg-purple-600/10 blur-[120px] transition-all duration-1000 animate-pulse" />
      <div className="absolute bottom-1/4 right-1/4 h-96 w-96 rounded-full bg-cyan-600/10 blur-[120px] transition-all duration-1000 animate-pulse" />
      
      <Canvas camera={{ position: [0, 0, 1] }}>
        <ParticleSphere />
      </Canvas>
    </div>
  );
}