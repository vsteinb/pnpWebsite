
const tile_size = 64;
const path_prefix = "/static/mining/game/";


// Speed in pixels per second
const playerFriction = .15;    // float in [0, 1] (slowing % per s)
const playerMaxSpeed = new Vector(20, 80);    // speed is already px/s, so on 'px per s' here :)
const playerXAcceleration = 3; // px per s
const playerFallAcceleration = 60; // px per s
const playerJumpDuration = 300;   // in ms
const playerJumpForce = 0.02; // px per s

const miningCooldown = 200;    // in ms