var camera, gui, container, scene, renderer,
        test, test1, stats, firstCamera,
        secondCamera, fileArray, combopairs,
        rotationController, zoomController, brightnessController;


//dat.gui for zoom/rotation/brightness

// function setupComboPairs(fileArray) {
//     "use strict";
//     function pairwise(list) {
//         var pairs = [((list.length * (list.length - 1)) / 2)],
//             pos = 0,
//             i = 0,
//             j = 0;
//         for (i = 0; i < list.length; i += 1) {
//             for (j = i; j < list.length; j += 1) {
//                 pairs[pos] = [list[i], list[j]];
//                 pos += 1;
//             }
//         }
//         return pairs;
//     }

//     var indexlist = [],
//         i;
//     for (i = 0; i < fileArray.length; i += 1) {
//         indexlist.push(i);
//     }

//     combopairs = pairwise(indexlist);

//     Array.prototype.shuffle = function () {
//         i = this.length;
//         var j, temp;
//         if (i === 0) {
//             return this;
//         }
//         while (i > 0) {
//             i -= 1;
//             j = Math.floor(Math.random() * (i + 1));
//             temp = this[i];
//             this[i] = this[j];
//             this[j] = temp;
//         }
//         return this;
//     };

//     combopairs.shuffle();
// }

function init(leftobj, rightobj) {
    "use strict";
    container = document.createElement('div');
    document.body.appendChild(container);
    scene = new THREE.Scene();

    // camera = new THREE.PerspectiveCamera( 45, window.innerWidth / window.innerHeight, 1, 50000 );
    // controls = new THREE.TrackballControls( camera );
    // controls.rotateSpeed = 5.0;
    // controls.zoomSpeed = 5;
    // controls.panSpeed = 2;
    // controls.noZoom = false;
    // controls.noPan = false;
    // controls.staticMoving = true;
    // controls.dynamicDampingFactor = 0.3;
    // scene.add( camera );
    // camera.position.z = 15000;
    // camera.lookAt(scene.position);

    var ambient = new THREE.AmbientLight(0x404040);
    scene.add(ambient);

    var manager = new THREE.LoadingManager();
    manager.onProgress = function (item, loaded, total) {
        console.log(item, loaded, total);
    };

    var material = new THREE.MeshLambertMaterial({
                                                  color: 0x404040,
                                                  side: THREE.DoubleSide
                                                  });

    var loader = new THREE.OBJLoader(manager);

    function loadLeftObject(objfile) {
        return new Promise(function (resolve) {
            loader.load(objfile, function (event) {
                var object = event;
                object.traverse(function (child) {
                    if (child instanceof THREE.Mesh) {
                        child.material = material;
                    }
                });
                var geometry = object.children[0].geometry;
                geometry.center();
                // var pc = new THREE.PointCloud( geometry, material );
                // pc.scale = new THREE.Vector3( 10, 10, 10 );
                // pc.position.set(10000, 0, 0);
                // scene.add ( pc );
                // test = pc;
                var mesh = new THREE.Mesh(geometry, material);
                mesh.position.set(10000, 0, 0);
                test = mesh;
                scene.add(mesh);

                // var hex = 0xff0000;
                // var bbox = new THREE.BoundingBoxHelper ( mesh, hex );
                // bbox.update();
                // scene.add(bbox);

                // mesh.scale = new THREE.Vector3( 10, 10, 10 );
                var hbox = new THREE.Box3().setFromObject(mesh);
                var newX, newY, newZ;
                newX = (hbox.max.x + hbox.min.x) / 2;
                newY = (hbox.max.y + hbox.min.y) / 2;
                newZ = (hbox.max.z + hbox.min.z) / 2;

                var cornerLight1 = new THREE.DirectionalLight(0x40f140);
                cornerLight1.position.set(hbox.max.x, hbox.max.y, hbox.max.z);
                scene.add(cornerLight1);

                var cornerLight2 = new THREE.DirectionalLight(0x40f040);
                cornerLight2.position.set(-hbox.max.x * 0.1, -hbox.max.y * 0.1, -hbox.max.z * 0.1);
                scene.add(cornerLight2);

                resolve([hbox.min.x, hbox.max.x, hbox.min.y, hbox.max.y, hbox.max.z, newX, newY, newZ]);
            });
        });
    }


    function loadRightObject(objfile) {
        return new Promise(function (resolve) {
            loader.load(objfile, function (event) {
                var object = event;
                object.traverse(function (child) {
                    if (child instanceof THREE.Mesh) {
                        child.material = material;
                    }
                });
                var geometry = object.children[0].geometry;
                geometry.center();
                var mesh = new THREE.Mesh(geometry, material);
                mesh.position.set(-10000, 0, 0);
                test1 = mesh;
                scene.add(mesh);

                // var hex = 0xff0000;
                // var bbox = new THREE.BoundingBoxHelper ( mesh, hex );
                // bbox.update();
                // scene.add(bbox);

                var hbox = new THREE.Box3().setFromObject(mesh);
                // mesh.scale = new THREE.Vector3( 10, 10, 10 );
                var newX, newY, newZ;
                newX = (hbox.max.x + hbox.min.x) / 2;
                newY = (hbox.max.y + hbox.min.y) / 2;
                newZ = (hbox.max.z + hbox.min.z) / 2;

                var cornerLight1 = new THREE.DirectionalLight(0x40f140);
                cornerLight1.position.set(hbox.max.x, hbox.max.y, hbox.max.z);
                scene.add(cornerLight1);

                var cornerLight2 = new THREE.DirectionalLight(0x40f040);
                cornerLight2.position.set(-hbox.max.x * 0.1, -hbox.max.y * 0.1, -hbox.max.z * 0.1);
                scene.add(cornerLight2);

                resolve([hbox.min.x, hbox.max.x, hbox.min.y, hbox.max.y, hbox.max.z, newX, newY, newZ]);
            });
        });
    }

  //This performs the loading of obj's!

    var file1, file2;
    function loadObjs(objFile1, objFile2) {
        return new Promise(function (resolve) {
            loadLeftObject(objFile1).then(function (planeArray) {
                var leftPlane = planeArray[0],
                    rightPlane = planeArray[1],
                    bottomPlane = planeArray[2],
                    topPlane = planeArray[3],
                    farPlane = planeArray[4],
                    xPos = planeArray[5],
                    yPos = planeArray[6],
                    innerWidth = (rightPlane - leftPlane) * 2,
                    innerHeight = (topPlane - bottomPlane) * 2;

                    // firstCamera = new THREE.OrthographicCamera( innerWidth / - 2, innerWidth / 2, innerHeight / 2, innerHeight / - 2, 1, farPlane*2.4);
                firstCamera = new THREE.PerspectiveCamera(45, innerWidth / innerHeight, farPlane * 5, farPlane * 10);
                firstCamera.position.set(xPos, yPos, farPlane * 7);
                scene.add(firstCamera);

                    // zoom controller
                // zoomController.onFinishChange(function (value) {
                //     firstCamera.position.set(xPos, yPos, farPlane * 7 * (value / 5));
                //     // secondCamera
                // });

                    // var firstCameraHelper = new THREE.CameraHelper ( firstCamera );
                    // testhelper = firstCameraHelper;
                    // scene.add(firstCameraHelper);

            }).catch(function (v) {
                console.log("Error has happened in loadLeftObject. :|");
                console.log(v);
            });

            loadRightObject(objFile2).then(function (planeArray) {
                var leftPlane = planeArray[0],
                    rightPlane = planeArray[1],
                    bottomPlane = planeArray[2],
                    topPlane = planeArray[3],
                    farPlane = planeArray[4],
                    xPos = planeArray[5],
                    yPos = planeArray[6],
                    innerWidth = (rightPlane - leftPlane) * 2,
                    innerHeight = (topPlane - bottomPlane) * 2;

                    // firstCamera = new THREE.OrthographicCamera( innerWidth / - 2, innerWidth / 2, innerHeight / 2, innerHeight / - 2, 1, farPlane*2.4);
                secondCamera = new THREE.PerspectiveCamera(45, innerWidth / innerHeight, farPlane * 5, farPlane * 10);

                secondCamera.position.set(xPos, yPos, farPlane * 7);

                // zoomController.onFinishChange(function (value) {
                //     secondCamera.position.set(xPos, yPos, farPlane * 7 * (value / 5));
                // });
                // var secondCameraHelper = new THREE.CameraHelper ( secondCamera );
                // testhelper1 = secondCameraHelper;
                scene.add(secondCamera);
                // scene.add(secondCameraHelper);
            }).catch(function (v) {
                console.log("Error has happened in loadRightObject. :|");
                console.log(v);
            });
            resolve("OK");
        });
    }

    //Ask server for first two sets of obj files

    function getObjFiles (argument) {
        var leftobj_url, rightobj_url;

        $.ajax({
            type:    "GET",
            url:     file1, //need to put the django url here
            success: function(objfiles) {
                leftobj_url = objfiles[0];
                rightobj_url = objfiles[1];
            },
            error:   function() {
                console.log("im a failure");
            }
        });

        console.log("Comparing " + file1 + " VS " + file2);
        console.log("Pair " + (currentpair_ndx + 1) + " of " + combopairs.length);


        loadObjs(leftobj_url, rightobj_url);
    }


    //This is going to be removed
    // var currentpair_ndx = 0;
    // function objFilePairTraversal() {
    //     if (currentpair_ndx === combopairs.length) {
    //         // var obj, i;
    //         // for ( i = scene.children.length - 1; i >= 0 ; i -- ) {
    //             // obj = scene.children[ i ];
    //             // scene.remove(obj);
    //         //}
    //         firstCamera.position.set(0, 0, 0);
    //         secondCamera.position.set(0, 0, 0);
    //         // printToCSV();
    //     } else {
    //         var currentpair = combopairs[currentpair_ndx],
    //             file1_ndx = currentpair[0],
    //             file2_ndx = currentpair[1];

    //         if (test && test1) {
    //             scene.remove(test);
    //             scene.remove(test1);
    //         }

    //         file1 = fileArray[file1_ndx];
    //         file2 = fileArray[file2_ndx];

    //         var getobj1, getobj2;

    //         $.ajax({
    //             type:    "GET",
    //             url:     file1,
    //             success: function(objfile) {
    //                 getobj1 = objfile;
    //             },
    //             error:   function() {
    //                 // An error occurred
    //             }
    //         });

    //         $.ajax({
    //             type:    "GET",
    //             url:     file2,
    //             success: function(objfile) {
    //                 getobj2 = objfile;                },
    //             error:   function() {
    //                 // An error occurred
    //             }
    //         });


    //         console.log("Comparing " + file1 + " VS " + file2);
    //         console.log("Pair " + (currentpair_ndx + 1) + " of " + combopairs.length);

    //         loadObjs(getobj1, getobj2);
    //         currentpair_ndx += 1;
    //     }
    //     // loadObjs(file1, file2).then(function (success) {
    //     //   currentpair_ndx++;
    //     // }).catch(function (v) {
    //     //   console.log("error has occured");
    //     // });
    // }

    stats = new Stats();
    stats.domElement.style.position = 'absolute';
    stats.domElement.style.bottom = '0px';
    stats.domElement.style.zIndex = 100;
    container.appendChild(stats.domElement);

    var answers = [["cell1", "cell2", "score"]];

    // function printToCSV() {
    //     var csvRows = [],
    //         l = answers.length,
    //         i;

    //     for (i = 0; i < l; i += 1) {
    //         csvRows.push(answers[i].join(','));
    //     }

    //     var csvString = csvRows.join("%0A"),
    //         a = document.createElement('a');
    //       a.href = 'data:attachment/csv,' + csvString;
    //       a.target = '_blank';
    //       a.download = 'androssresults.csv';

    //     document.body.appendChild(a);
    //     a.click();

    //     disableButtons();
    // }


    // function disableButtons() {
    //     $( "#confirm" ).button( "disable");
    // }

    var selection = 0;

    /*$(function () {
        //Read in whatever choice was selected and then reset selection to 0 and disable button
        $("input[type=submit], a, button")
            .button()
            .click(function (event) {
                event.preventDefault();
                var datastring = '&rating='+selection;
                //Save the option
                 $.ajax({
                   type: "POST",
                   url: "newRating",
                   data : datastring,
                   success: function (msg){
                       //alert("Data Saved: " + msg);

                   }
                 });
                // answers.push([file1.substring(6), file2.substring(6), selection]);

                selection = 0;
                $("#confirm").button("disable");
                //ok we'll need to test this
                //getObjFiles();
                // objFilePairTraversal();
            });

        $('#radio').click(function (evt) {
            $("input[type='radio']:checked").each(function () {
                var idVal = $(this).attr("id");
                // console.log($("label[for='"+idVal+"']").text());
                selection = $("label[for='" + idVal + "']").text();
                $("#confirm").button("enable", true);
                evt.stopPropagation();
                evt.preventDefault();
            });
        });

        //Disable on startup
        if (selection === 0) {
            $("#confirm").button("disable");
        }
    });*/

    $(document).ready(function () {
        $(function () {
            $("#radio").buttonset();
        });
    });

    $(document).keypress(function (event) {
        if (event.keyCode === 49) {
            document.getElementById("radio1").checked = true;
            $('#radio1').click();
            $("#radio").buttonset("refresh");
        }
    });

    $(document).keypress(function (event) {
        if (event.keyCode === 50) {
            document.getElementById("radio2").checked = true;
            $('#radio2').click();
            $("#radio").buttonset("refresh");
        }
    });

    $(document).keypress(function (event) {
        if (event.keyCode === 51) {
            document.getElementById("radio3").checked = true;
            $('#radio3').click();
            $("#radio").buttonset("refresh");
        }
    });

    $(document).keypress(function (event) {
        if (event.keyCode === 52) {
            document.getElementById("radio4").checked = true;
            $('#radio4').click();
            $("#radio").buttonset("refresh");
        }
    });

    $(document).keypress(function (event) {
        if (event.keyCode === 53) {
            document.getElementById("radio5").checked = true;
            $('#radio5').click();
            $("#radio").buttonset("refresh");
        }
    });

    //Bug: Buttons will remain "checked" after confirmation
    //but user will still have to hit or click the button to continue...
    $(document).keypress(function (event) {
        if (event.keyCode === 13) {
            $('#confirm').click();
            // $("radio1").removeAttr('checked');
            // $("radio2").removeAttr('checked');
            // $("radio3").removeAttr('checked');
            // $("radio4").removeAttr('checked');
            // $("radio5").removeAttr('checked');
            // $( "#radio" ).buttonset("refresh");
        }
    });

    //objFilePairTraversal();
    loadObjs(leftobj, rightobj);

    renderer = new THREE.WebGLRenderer({alpha: true});
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setClearColor(0xffffff);
    renderer.autoClear = false;
    renderer.autoClearColor = true;
    container.appendChild(renderer.domElement);

    window.addEventListener('resize', function () {
        var WIDTH = window.innerWidth,
            HEIGHT = window.innerHeight;
        renderer.setSize(WIDTH, HEIGHT);
    });
}

var rotationSpeedScale = 0.1;
var rotateSpeed = 0.015;
function animate() {
    "use strict";
    requestAnimationFrame(animate);
    if (test && test1) {

        // rotationController.onFinishChange(function (value) {
        //     rotateSpeed = rotationSpeedScale * (value / 1000);
        // });

        test.rotation.y += rotateSpeed;
        test1.rotation.y -= rotateSpeed;
    }

    if (firstCamera && secondCamera) {
        renderer.setViewport(1, 1, window.innerWidth / 2, window.innerHeight);
        renderer.render(scene, firstCamera);

        renderer.setViewport(window.innerWidth / 2, 1, window.innerWidth / 2, window.innerHeight);
        renderer.render(scene, secondCamera);
    }

    stats.update();
    // controls.update();
    // renderer.render(scene, camera);
}


// function initializeFileArray() {
//     "use strict";
//     return new Promise(function (resolve) {
//         $.getJSON("cells.json", function (json) {
//             resolve(json);
//         });
//     });
// }

// This part + initializeFileArray and setupComboPairs
// will be removed since file paths will be provided
// from the django server
//This too will be removed...
// initializeFileArray().then(function (jsondata) {
//     "use strict";
//     fileArray = jsondata;
//     // This will be removed
//     setupComboPairs(jsondata);
//     init();
//     animate();
// }).catch(function (v) {
//     "use strict";
//     console.log(v);
//     console.log("Error loading cells.json");
// });
