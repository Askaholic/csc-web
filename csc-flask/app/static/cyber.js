var numConnectors = Math.floor(Math.random() * 6 + 4);
var allPaths = []

$(document).ready(
  function() {
    registerHandlers();
    generateAllPaths();
    updateCanvas(document.getElementById("background"));
  }
);

function registerHandlers() {
  registerCheckboxHandler();
  registerResizeHandler();
}

function registerCheckboxHandler() {
  $("#create-account").change(
    function() {
      target = $(this).attr("data-target");
      if ($(this).is(":checked"))
        $(target).show(120);
      else
        $(target).hide(120);
    }
  );
}

function registerResizeHandler() {
  $(window).resize(
    function() {
      updateCanvas(document.getElementById("background"));
    }
  );
}

function generateAllPaths() {
  var prevPath = []
  const basePathLength = 5;
  for(var i = 0; i < 4; i++) {
    for(var c=0; c < numConnectors; c++) {
      var path = [];
      var initial = 0;
      var validDirections = [];
      if(c == 0) {
        initial = Math.floor(Math.random() * 2) + 1;
        validDirections = [0, 1, 2];
      }
      else if(c == numConnectors - 1) {
        initial =  Math.floor(Math.random() * 2) + 6;
        validDirections = [6, 7, 0];
      }
      else if (c < (numConnectors - 1) / 2 ) {
        validDirections = [0, 1, 2];
      }
      else if (c > (numConnectors - 1) / 2 ){
        validDirections = [6, 7, 0]
      }
      else {
        validDirections = [6, 7, 0, 1, 2];
      }
      var pathlen = basePathLength + Math.floor(Math.random() * 3)
      path = generatePath(pathlen, initial, validDirections, prevPath);
      allPaths.push(path);
      prevPath = path;
    }
  }
}

function updateCanvas(canvas) {
  setupCanvas(canvas);
  const ctx = canvas.getContext("2d");
  const h = canvas.height;
  const w = canvas.width;
  const circuitH = 200;
  const circuitW = 200;
  const cornerH = circuitH / 10;
  const cornerW = circuitW / 10;
  ctx.lineWidth = 5;
  drawCircuitCenter(canvas, circuitW, circuitH, cornerW, cornerH);
  ctx.lineWidth = 3;
  drawArms(canvas, circuitW, circuitH, cornerW, cornerH, numConnectors);
}

function line(ctx, x, y) {
  ctx.lineTo(x, y);
  ctx.moveTo(x, y);
}

function circle(ctx, centerX, centerY, radius) {
  ctx.beginPath();
  ctx.arc(centerX, centerY, radius, 0, 2 * Math.PI, false);
}

function setupCanvas(canvas) {
  const h = $( window ).height();
  const w = $( window ).width();

  canvas.height = h;
  canvas.style.height = h;
  canvas.width = w;
  canvas.style.width = w;

  const ctx = canvas.getContext("2d")
  ctx.clearRect(0, 0, w, h);
}

function drawCircuitCenter(canvas, circuitW, circuitH, cornerW, cornerH) {
  ctx = canvas.getContext("2d");
  ctx.lineCap = "round"
  h = canvas.height;
  w = canvas.width;
  centerX = w / 2;
  centerY = h / 2;
  newX = centerX - (circuitW / 2);
  newY =  centerY - (circuitH / 2);
  ctx.translate(newX, newY);
  ctx.moveTo(cornerW, 0);
  line(ctx, 0, cornerH);
  line(ctx, 0, circuitH - (cornerH));
  line(ctx, cornerW, circuitH);
  line(ctx, circuitW - (cornerW), circuitH);
  line(ctx, circuitW, circuitH - (cornerH));
  line(ctx, circuitW, cornerH);
  line(ctx, circuitW - cornerW, 0)
  line(ctx, cornerW, 0)
  ctx.stroke();
  ctx.translate(-newX, -newY);
}

function drawArms(canvas, circuitW, circuitH, cornerW, cornerH, numConnectors) {
    ctx = canvas.getContext("2d");
    const h = canvas.height;
    const w = canvas.width;

    centerX = w / 2;
    centerY = h / 2;
    cRadius = cornerH / 3;
    cDiameter = cRadius * 2;
    spaceX = ((circuitW - cornerW * 2) - cDiameter * numConnectors) / (numConnectors - 1);
    spaceY = ((circuitH - cornerH * 2) - cDiameter * numConnectors) / (numConnectors - 1);
    gapX = cornerW / 2;
    gapY = cornerH / 2;
    newX = -(circuitW / 2) - gapX - cornerW;
    newY = -(circuitH / 2) - gapY - cornerH;

    ctx.translate(centerX, centerY);
    for(var side = 0; side < 4; side++) {
      ctx.rotate(Math.PI / 2);
      ctx.translate(newX, newY);
      startOffestX = gapX + cDiameter + cornerW;
      startOffestY = gapY + cDiameter + cornerH;
      var frameX = 0;
      var frameY = startOffestY + cRadius;
      ctx.translate(frameX, frameY);
      for(var c = 0; c < numConnectors; c++) {
        var newOffest = cDiameter + spaceY;
        path = allPaths[side * numConnectors + c];
        var numLength = c;
        if (c > numConnectors / 2) {
          numLength = numConnectors - c;
        }
        arm(ctx, 20 * (numLength + 1), path)
        ctx.translate(0, newOffest);
        frameY += newOffest;
      }
      ctx.translate(-frameX, -frameY)
      ctx.translate(-newX, - newY)
    }
    ctx.translate(-centerX, -centerY);
}

function arm(ctx, segmentLength, path) {
  circle(ctx, cRadius, cRadius, cRadius);
  ctx.stroke();
  var adjustedY = -cRadius * Math.sin(path[0] * Math.PI / 4);
  var adjustedX = 0;
  if(path[0] == 2 || path[0] == 6) {
    adjustedX = cRadius;
  }
  ctx.translate(adjustedX, adjustedY)
  ctx.moveTo(0, cRadius);
  var prevX = 0;
  var prevY = cRadius;
  for(var c = 0; c < path.length; c++) {
    prevX -= segmentLength * Math.cos(path[c] * Math.PI / 4);
    prevY -= segmentLength * Math.sin(path[c] * Math.PI / 4);
    line(ctx, prevX, prevY);
  }
  ctx.stroke();
  lastDir = path[path.length-1]
  circle(ctx, prevX - cRadius * Math.cos(lastDir * Math.PI / 4), prevY - cRadius * Math.sin(lastDir * Math.PI / 4), cRadius);
  if(lastDir % 2 == 0) {
    ctx.stroke();
  }
  else {
    ctx.fill();
  }
  ctx.translate(-adjustedX, -adjustedY)
}

function generatePath(length, initial, validDirections, prevPath) {
  path = [initial];
  var prev = initial;
  for(var i = 1; i < length; i++) {
    var pathOptions = generatePathOptions(prev, validDirections, prevPath, i)
    if(pathOptions.length==0) {
      console.log("No path options!\n" + prev + ", " + validDirections + ", " + prevPath + ", " + i);
    }
    var step = Math.floor(Math.random() * pathOptions.length);
    path.push(pathOptions[step]);
    prev = path[i];
  }
  return path;
}

function generatePathOptions(dirCurrent, validDirections, prevPath, iPrev) {
  var pathOptions = [];
  prevPathDir = 8;
  if(iPrev < prevPath.length) {
    prevPathDir = prevPath[iPrev];
    if(dirCurrent < 4 && dirCurrent <= prevPathDir) {
      pathOptions.push(dirCurrent);
    }
    else if((dirCurrent > 4 || dirCurrent == 0) && dirCurrent >= prevPathDir) {
      pathOptions.push(dirCurrent);
    }
    for(var i = 0; i < validDirections.length; i++) {
      if(((dirCurrent + 7) % 8 == validDirections[i]) && ((dirCurrent + 7) % 8 >= prevPathDir)) {
        pathOptions.push((dirCurrent + 7) % 8);
      }
      else if(((dirCurrent + 1) % 8 == validDirections[i]) && ((dirCurrent + 1) % 8 <= prevPathDir)) {
        pathOptions.push((dirCurrent + 1) % 8);
      }
    }
  }
  else {
    pathOptions.push(dirCurrent);
    for(var i = 0; i < validDirections.length; i++) {
      if(((dirCurrent + 7) % 8 == validDirections[i])) {
        pathOptions.push((dirCurrent + 7) % 8);
      }
      else if((dirCurrent + 1) % 8 == validDirections[i]) {
        pathOptions.push((dirCurrent + 1) % 8);
      }
    }
  }
  return pathOptions;
}
