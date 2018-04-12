// Balls animation made in JavaScript.
// Utilizing JQuery.

// By Adam Shechter    adam.s.develop@gmail.com

var circlesArr = [];

// final variable?
const COLORS = [
	"#000000", "#FF0000", 
	"#00FF00", "#0000FF", 
	"#FFFF00", "#00FFFF", 
	"#FF00FF", "#C0C0C0"
];

function createCanvasObject() {
    var width = window.innerWidth;
    var height = window.innerHeight;
    var canvasObject = document.createElement("CANVAS");
    canvasObject.id = "balls";
    // canvasObject.height = height * 0.8;
    // canvasObject.width = width * 0.8;
    canvasObject.height = height;
    canvasObject.width = width;
    var canvasdiv = document.getElementsByClassName("canvasspace");
    canvasdiv[0].appendChild(canvasObject);
}

function Circle(x, y, name) {
    this.x = x;
    this.y = y;
    // this.radius = Math.floor(Math.random()*15)+3;
    // this.xvelocity = Math.floor(Math.random()*5)+0.5;
    // this.yvelocity = Math.floor(Math.random()*5)+0.5;
    this.radius = 100;
    this.xvelocity = 0;
    this.yvelocity = 0;
    this.name = name;
    colorn = Math.floor(Math.random() * 8);
    this.color = COLORS[colorn];
}

// NOTE: The main part, does stuff instead of usingSetTimeout
var requestAnimationFrame = 
	window.requestAnimationFrame ||
    window.mozRequestAnimationFrame ||
    window.webkitRequestAnimationFrame ||
    window.msRequestAnimationFrame;

createCanvasObject();

var canvas = document.getElementById('balls');
var ctx = canvas.getContext("2d");

function renderCircle() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    for (var i = 0; i < circlesArr.length; i += 1) {
        ctx.beginPath();
        ctx.arc(circlesArr[i].x, circlesArr[i].y, circlesArr[i].radius, 0, 2 * Math.PI);
        ctx.fillStyle = circlesArr[i].color;
        ctx.fill();
        ctx.closePath();
		ctx.font = '15pt Calibri';
		ctx.fillStyle = 'white';
		ctx.textAlign = 'center';
		ctx.fillText(circlesArr[i].name, circlesArr[i].x, circlesArr[i].y + 5);

        if (((circlesArr[i].y) > canvas.height) || ((circlesArr[i].y) < 0)) {
            // circlesArr[i].yvelocity *= -1;
            circlesArr[i].yvelocity = 0;
        }

        if (((circlesArr[i].x) >= canvas.width) || ((circlesArr[i].x) <= 0)) {
            // circlesArr[i].xvelocity *= -1;
            circlesArr[i].xvelocity = 0;
        }

        circlesArr[i].y += circlesArr[i].yvelocity;
        circlesArr[i].x += circlesArr[i].xvelocity;

        for (var idx = 0; idx < circlesArr.length; idx += 1) {
            // skip over if it's the same circle with same index number
            if (idx === i) {
                continue;
            } else {
                // detection collision
                // console.log('in detection collision', i, idx);
                var xdist = Math.pow((circlesArr[i].x - circlesArr[idx].x), 2);
                var ydist = Math.pow((circlesArr[i].y - circlesArr[idx].y), 2);
                var radSqr = Math.pow((circlesArr[i].radius + circlesArr[idx].radius), 2);

                if ((xdist + ydist) <= radSqr) {
                    // collision
                    var colorn;

                    if ((circlesArr[i].radius < 50) || (circlesArr[idx].radius < 50)) {
                        // console.log('less than 50 collision', i, idx);
                        if (circlesArr[i].radius > circlesArr[idx].radius) {
                            if (circlesArr[i].radius < 50) {
                                circlesArr[i].radius += (circlesArr[idx].radius / 2);
                            }

                            colorn = Math.floor(Math.random() * 8);
                            while ((COLORS[colorn] == circlesArr[i].color) || (COLORS[colorn] == circlesArr[idx].color)) {
                                colorn = Math.floor(Math.random() * 8);
                            }

                            circlesArr[i].color = COLORS[colorn];
                            circlesArr.splice(idx, 1);
                        } else if (circlesArr[i].radius <= circlesArr[idx].radius) {
                            if (circlesArr[idx].radius < 50) {
                                circlesArr[idx].radius += (circlesArr[i].radius / 2);
                            }

                            colorn = Math.floor(Math.random() * 8);
                            while ((COLORS[colorn] == circlesArr[i].color) || (COLORS[colorn] == circlesArr[idx].color)) {
                                colorn = Math.floor(Math.random() * 8);
                            }
                            circlesArr[idx].color = COLORS[colorn];
                            circlesArr.splice(i, 1);
                        }
                    } else {
                        // Large balls bounce off one another.
                        // console.log('greater than 50 radius collision', i, idx);
                        // circlesArr[i].xvelocity *= -1;
                        // circlesArr[i].yvelocity *= -1;
                        // circlesArr[idx].xvelocity *= -1;
                        // circlesArr[idx].yvelocity *= -1;
                    }

                    break;
                }
            }
        }
    }

    requestAnimationFrame(renderCircle);
}

function makeCircle(x, y, name) {
    var newCircle = new Circle(x, y, name);
    // var randomDirectionX = Math.floor(Math.random() * 2),
    //     randomDirectionY = Math.floor(Math.random() * 2);

    // if (randomDirectionX != 1)
    //     newCircle.xvelocity *= -1;
    // if (randomDirectionY != 1)
    //     newCircle.yvelocity *= -1;

    circlesArr.push(newCircle);

    // console.log('X ' + newCircle.x);
    // console.log('Y ' + newCircle.y);
    // console.log('Xvel ' + newCircle.xvelocity);
    // console.log('Yvel ' + newCircle.yvelocity);
}

function popup() {
	var name = prompt('Type your nickname');

    if (!name || name == '') {
    	popup();
    } else {
    	return name;
    }
}

$(document).ready(function() {
	// Disabled circle generation
    // makeCircle((window.innerWidth / 2), (window.innerHeight / 2));
    renderCircle();

    var name = popup();
    makeCircle((window.innerWidth / 2), (window.innerHeight / 2), name);

    $('#balls').click(function(event) {
        console.log('canvas clicked');
        var x = event.clientX; // Get the horizontal coordinate
        var y = event.clientY; // Get the vertical coordinate
        makeCircle(x, y);

    });
});
