from fasthtml.common import *

app = FastHTML()
rt = app.route

@rt('/')
def get():
    return Html(
        Head(
            Title('Minecraft Clone'),
            Script(src='https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js'),
            Script(src='https://unpkg.com/htmx.org@1.6.1'),
            Script(src='https://unpkg.com/htmx.org/dist/ext/json-enc.js'),
            Style('''
                body { margin: 0; overflow: hidden; }
                canvas { display: block; }
            ''')
        ),
        Body(
            Div(id='minecraft-game'),
            Script('''
                const scene = new THREE.Scene();
                const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
                const renderer = new THREE.WebGLRenderer();
                renderer.setSize(window.innerWidth, window.innerHeight);
                document.body.appendChild(renderer.domElement);

                const geometry = new THREE.BoxGeometry();

                function createBlock(x, y, z, color) {
                    const material = new THREE.MeshBasicMaterial({ color });
                    const block = new THREE.Mesh(geometry, material);
                    block.position.set(x, y, z);
                    return block;
                }

                const blocks = [];
                for (let x = -5; x <= 5; x++) {
                    for (let z = -5; z <= 5; z++) {
                        const color = Math.random() * 0xffffff;
                        const block = createBlock(x, 0, z, color);
                        scene.add(block);
                        blocks.push(block);
                    }
                }

                camera.position.set(0, 10, 15);
                camera.lookAt(0, 0, 0);

                const raycaster = new THREE.Raycaster();
                const mouse = new THREE.Vector2();

                function onMouseClick(event) {
                    mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
                    mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;
                    raycaster.setFromCamera(mouse, camera);

                    const intersects = raycaster.intersectObjects(blocks);
                    if (intersects.length > 0) {
                        const intersect = intersects[0];
                        if (event.button === 0) {  // Left click
                            const newBlock = createBlock(
                                Math.round(intersect.point.x + intersect.face.normal.x),
                                Math.round(intersect.point.y + intersect.face.normal.y),
                                Math.round(intersect.point.z + intersect.face.normal.z),
                                Math.random() * 0xffffff
                            );
                            scene.add(newBlock);
                            blocks.push(newBlock);
                        } else if (event.button === 2) {  // Right click
                            scene.remove(intersect.object);
                            blocks.splice(blocks.indexOf(intersect.object), 1);
                        }
                    }
                }

                document.addEventListener('mousedown', onMouseClick, false);
                document.addEventListener('contextmenu', (event) => event.preventDefault(), false);

                document.addEventListener('wheel', (event) => {
                    camera.position.z += event.deltaY * 0.05;
                });

                const moveSpeed = 0.1;
                document.addEventListener('keydown', (event) => {
                    switch (event.key) {
                        case 'w':
                            camera.position.z -= moveSpeed;
                            break;
                        case 's':
                            camera.position.z += moveSpeed;
                            break;
                        case 'a':
                            camera.position.x -= moveSpeed;
                            break;
                        case 'd':
                            camera.position.x += moveSpeed;
                            break;
                        case ' ':
                            camera.position.y += moveSpeed;
                            break;
                        case 'Shift':
                            camera.position.y -= moveSpeed;
                            break;
                    }
                });

                let time = 0;
                function animate() {
                    requestAnimationFrame(animate);
                    time += 0.01;
                    const r = Math.sin(time) * 0.5 + 0.5;
                    const g = Math.sin(time + 2) * 0.5 + 0.5;
                    const b = Math.sin(time + 4) * 0.5 + 0.5;
                    scene.background = new THREE.Color(r, g, b);
                    renderer.render(scene, camera);
                }

                animate();
            ''', type='module')
        )
    )

serve()