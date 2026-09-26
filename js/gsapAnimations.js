/**
 * GSAP ScrollTrigger Scrollytelling Animations
 */

export function initGsapAnimations(threeScene) {
  gsap.registerPlugin(ScrollTrigger);

  const { foodMasterGroup, peelMeshLeft, peelMeshRight, pulpMesh, nutrientGroup, ringMesh } = threeScene;

  // Timeline 1: Hero to 3D Dissection (Separates peel and expands molecular cloud)
  gsap.timeline({
    scrollTrigger: {
      trigger: "#dissection",
      start: "top bottom",
      end: "center center",
      scrub: 1,
    }
  })
  .to(foodMasterGroup.position, { x: 2.0, y: 0, z: 0.5 })
  .to(peelMeshLeft.position, { x: -0.9, y: 0.4, z: 0.2 }, 0)
  .to(peelMeshRight.position, { x: 0.9, y: -0.4, z: -0.2 }, 0)
  .to(pulpMesh.scale, { x: 0.85, y: 0.85, z: 0.85 }, 0)
  .to(nutrientGroup.scale, { x: 1.6, y: 1.6, z: 1.6 }, 0)
  .to(ringMesh.rotation, { z: Math.PI }, 0);

  // Timeline 2: Dissection to Scanner (Shrinks 3D model into ambient background)
  gsap.timeline({
    scrollTrigger: {
      trigger: "#scanner",
      start: "top bottom",
      end: "top center",
      scrub: 1,
    }
  })
  .to(foodMasterGroup.position, { x: -3.5, y: 2.0, z: -3 }, 0)
  .to(foodMasterGroup.scale, { x: 0.5, y: 0.5, z: 0.5 }, 0);

  // Timeline 3: Dissection Diagnostic Step Highlighting
  ScrollTrigger.create({
    trigger: "#dissection",
    start: "top 60%",
    end: "bottom 40%",
    onToggle: self => {
      const step = document.getElementById('step-skin');
      if (step) step.classList.toggle('active', self.isActive);
    }
  });
}
