var numConnectors = Math.ceil(Math.random() * 6 + 3);

$(document).ready(
  function() {
    registerHandlers();
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

function updateCanvas(canvas) {
  setupCanvas(canvas);
  ctx = canvas.getContext("2d");
  h = canvas.height;
  w = canvas.width;
  circuitH = h / 5;
  circuitW = h / 5;
  cornerH = circuitH / 10;
  cornerW = circuitW / 10;
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
  h = $( window ).height();
  w = $( window ).width();

  canvas.height = h;
  canvas.style.height = h;
  canvas.width = w;
  canvas.style.width = w;

  ctx = canvas.getContext("2d")
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
    h = canvas.height;
    w = canvas.width;

    centerX = w / 2;
    centerY = h / 2;
    cRadius = 8;
    cDiameter = cRadius * 2;
    spaceX = ((circuitW - cornerW * 2) - cDiameter * numConnectors) / (numConnectors - 1);
    spaceY = ((circuitH - cornerH * 2) - cDiameter * numConnectors) / (numConnectors - 1);
    gapX = cornerW / 2;
    gapY = cornerH / 2;
    newX = - (circuitW / 2) - gapX - cornerW;
    newY = - (circuitH / 2) - gapY - cornerH;

    ctx.translate(centerX, centerY);
    for(side = 0; side < 4; side++) {
      ctx.rotate(Math.PI / 2);
      ctx.translate(newX, newY);
      startOffestX = gapX + cDiameter + cornerW;
      startOffestY = gapY + cDiameter + cornerH;
      // Left side
      frameX = cRadius;
      frameY = startOffestY + cDiameter;
      ctx.translate(frameX, frameY);
      for(c = 0; c < numConnectors; c++) {
        newOffest = cDiameter + spaceY;
        circle(ctx, 0, 0, cRadius);
        ctx.stroke();
        ctx.moveTo(-cRadius, 0);
        ctx.lineTo(-20 - (c * 5), 0);
        ctx.stroke();
        ctx.translate(0, newOffest);
        frameY += newOffest;
      }
      ctx.translate(-frameX, -frameY)
      ctx.translate(-newX, - newY)
    }
    ctx.translate(-centerX, -centerY);
    // ctx.translate(newX, newY);
    // startOffestX = gapX + cDiameter + cornerW;
    // startOffestY = gapY + cDiameter + cornerH;
    // // Left side
    // frameX = cRadius;
    // frameY = startOffestY + cDiameter;
    // ctx.translate(frameX, frameY);
    // for(c = 0; c < numConnectors; c++) {
    //   newOffest = cDiameter + spaceY;
    //   circle(ctx, 0, 0, cRadius);
    //   ctx.stroke();
    //   ctx.moveTo(-cRadius, 0);
    //   ctx.lineTo(-20 - (c * 5), 0);
    //   ctx.stroke();
    //   ctx.translate(0, newOffest);
    //   frameY += newOffest;
    // }
    // ctx.translate(-frameX, -frameY)
    // // Bottom
    // frameX = startOffestX + cDiameter;
    // frameY = cRadius + startOffestY * 2 + circuitH - (cornerH * 2);
    // ctx.translate(frameX, frameY);
    // for(c = 0; c < numConnectors; c++) {
    //   newOffest = cDiameter + spaceX;
    //   circle(ctx, 0, 0, cRadius);
    //   ctx.stroke();
    //   ctx.translate(newOffest, 0);
    //   frameX += newOffest;
    // }
    // ctx.translate(-frameX, -frameY)
    // // Top
    // frameX = startOffestX + cDiameter;
    // frameY = cRadius;
    // ctx.translate(frameX, frameY);
    // for(c = 0; c < numConnectors; c++) {
    //   newOffest = cDiameter + spaceX;
    //   circle(ctx, 0, 0, cRadius);
    //   ctx.stroke();
    //   ctx.translate(newOffest, 0);
    //   frameX += newOffest;
    // }
    // ctx.translate(-frameX, -frameY)
    // // Right
    // frameX = cRadius + startOffestX * 2 + circuitW - (cornerW * 2);
    // frameY = startOffestY + cDiameter;
    // ctx.translate(frameX, frameY);
    // for(c = 0; c < numConnectors; c++) {
    //   newOffest = cDiameter + spaceY;
    //   circle(ctx, 0, 0, cRadius);
    //   ctx.stroke();
    //   ctx.translate(0, newOffest);
    //   frameY += newOffest;
    // }
    // ctx.translate(-frameX, -frameY)
    // ctx.translate(-newX, -newY);
}
