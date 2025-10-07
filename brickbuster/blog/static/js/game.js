var length = 17
var width = 8
var lost = true
var speed_up = false
var game_paused = false
var keyState = {}
var speed = 80
var hardness_factor = 1
var score_per_line = [0, 40, 100, 300, 1200]
var difficulties = ["normal", "hard", "insane"]
var speeds = [80, 40, 20]
var hardness_factors = [1, 2, 4]
var score_element = document.getElementById("score")
var object_types = ["snake_right",
                    "snake_left",
                    "cube",
                    "line",
                    "pyramid",
                    "corner_left",
                    "corner_right"]
var rotation = ["up", "down", "left", "right"]
var colors = ["wine", "sand", "green", "blue", "orange", "pink"]
var forms = {
  snake_right : [[[1, 4], [2, 3], [2, 4], [3, 3]],
                 [[2, 2], [2, 3], [3, 3], [3, 4]]],
  snake_left: [[[1, 3], [2, 3], [2, 4], [3, 4]],
               [[2, 3], [2, 4], [3, 2], [3, 3]]],
  cube : [[[2, 3], [2, 4], [3, 3], [3, 4]]],
  line : [[[0, 3], [1, 3], [2, 3], [3, 3]],
          [[3, 2], [3, 3], [3, 4], [3, 5]]],
  pyramid : [[[1, 3], [2, 3], [2, 4], [3, 3]],
             [[2, 2], [2, 3], [2, 4], [3, 3]],
             [[1, 3], [2, 2], [2, 3], [3, 3]],
             [[1, 3], [2, 2], [2, 3], [2, 4]],],
  corner_right : [[[1, 3], [1, 4], [2, 3], [3, 3]],
                  [[2, 2], [2, 3], [2, 4], [3, 4]],
                  [[1, 3], [2, 3], [3, 2], [3, 3]],
                  [[1, 2], [2, 2], [2, 3], [2, 4]],],
  corner_left : [[[1, 2], [1, 3], [2, 3], [3, 3]],
                 [[1, 4], [2, 2], [2, 3], [2, 4]],
                 [[1, 3], [2, 3], [3, 3], [3, 4]],
                 [[2, 2], [2, 3], [2, 4], [3, 2]],]
}
var score_saved_sign = document.getElementsByClassName("score-saved")[0]
var game_over_sign
var current_speed
var object_type
var coords_variants
var coords_exact
var current_coords
var rotation
var new_coords
var classes
var rows_deleted
var score

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function choose_difficulty(difficulty){
  if (lost == false){return null}
  for (i in difficulties){
    difficulty_type = difficulties[i]
    var button = document.getElementById(difficulty_type)
    if (difficulty == difficulty_type){
      hardness_factor = hardness_factors[i]
      speed = speeds[i]
      try {button.classList.remove('btn-dimmed')}
      catch {}
    }
    else {
      button.classList.add('btn-dimmed')
    }
  }
}

function spawn_object(){
  coords_variants = next_coords_variants
  rotation = next_rotation
  coords_exact = next_coords_exact
  color = next_color
  for (let i = 0; i < 4; i++){
    coord = coords_exact[i]
    object = get_element(coord[0], coord[1])
    object.classList.add(color, "filled", "current")
  }
  clear_sub_table()
  generate_next_object()
}

function clear_sub_table(){
  elements = document.getElementsByClassName("table-sub")
  for (let row = 0; row < 5; row++){
    for (let col = 1; col < 6; col++){
      id = "sub" + row + "_" + col
      element = document.getElementById(id)
      element.removeAttribute("class")
    }
  }
}

var i = 1
function generate_next_object(){
  next_object_type = object_types[Math.floor(Math.random() * object_types.length)];
  i += 1
  next_color = colors[Math.floor(Math.random() * colors.length)];
  next_coords_variants = []
  next_coords_variants = forms[next_object_type]
  next_rotation = Math.floor(Math.random() * Math.floor(next_coords_variants.length));
  next_coords_exact = next_coords_variants[next_rotation];
  for (let i = 0; i < 4; i++){
    next_coord = next_coords_exact[i]
    id  = "sub" + next_coord[0] + '_' + next_coord[1]
    object = document.getElementById(id)

    object.classList.add(next_color, "filled")
  }
}

function can_rotate(){
  for (i = 0; i < 4; i++){
    new_row = current_coords[i][0] - coords_exact[i][0] + coords_variants[new_rotation][i][0]
    new_col = current_coords[i][1] - coords_exact[i][1] + coords_variants[new_rotation][i][1]
    new_id = new_row + '_' + new_col
    new_item = document.getElementById(new_id)
    if (new_item.classList.contains("filled") && !new_item.classList.contains("current")){ return false }
  }
  return true
}

function rotate(){
  current_coords = []
  new_coords = []
  items = document.getElementsByClassName("current")
  for (item_id = 0; item_id < 4; item_id++){
    row = parseInt(items[item_id].id.split('_')[0])
    col = parseInt(items[item_id].id.split('_')[1])
    current_coords.push([row, col])
  }
  if (rotation == (coords_variants.length-1)){
    new_rotation = 0;
  } else { new_rotation = rotation + 1 }
  classes = Array.from(items[0].classList)
  if (can_rotate()){
    for (i = 0; i < 4; i++){
      old_item = items[0]
      old_item.removeAttribute("class")
    }
    for (i = 0; i < 4; i++){
      new_row = current_coords[i][0] - coords_exact[i][0] + coords_variants[new_rotation][i][0]
      new_col = current_coords[i][1] - coords_exact[i][1] + coords_variants[new_rotation][i][1]
      new_id = new_row + '_' + new_col
      new_item = document.getElementById(new_id)
      for (j = 0; j < 3; j++){
        new_item.classList.add(classes[j])
      }
    }
    coords_exact = coords_variants[new_rotation]
    rotation = new_rotation
  }
}

function get_element(row, col){
  let id = row + "_" + col
  return document.getElementById(id);
}

async function move_object() {
  items = document.getElementsByClassName("current")
  classes = Array.from(items[0].classList)
  while (await can_move_y()){
    if (!game_paused){
      for (let item_id = 3; item_id > -1; item_id--) {
        item = items[item_id]
        id = item.id
        next_id = (parseInt(id.split('_')[0]) + 1) + '_' + id.split('_')[1]
        var next_item = document.getElementById(next_id)
        items[item_id].removeAttribute("class")
        for (j = 0; j < 3; j++){
          next_item.classList.add(classes[j])
        }
      }
      for (g = 1; g < 11; g++){
        if (keyState[40]){ await sleep(5) }
        else {
          await sleep(current_speed);
        }
      }
      speed_up = false
    } else {await sleep(10);}
  }
  rows_deleted = 0
  await check_rows(length)
  if (rows_deleted != 0){
    add_score()
  }
}

function add_score(){
  score += score_per_line[rows_deleted]*hardness_factor
  score_element.innerHTML = score
}

async function check_rows(start_row){
  for (let row = start_row; row > 3; row--){
    for (let col = 0; col < width; col++){
      element = get_element(row, col)
      if (!element.classList.contains("filled")) {
        await check_rows(row-1)
        return null;
      }
    }
    rows_deleted += 1
    await delete_row(row)
    await move_down(row)
    await check_rows(start_row)
  }
}

async function delete_row(row){
  await sleep(100)
  for (color_id in colors){
    for (let col = 0; col < width; col++){
      element = get_element(row, col)
      element.removeAttribute("class");
      element.classList.add(colors[color_id])
    }
    await sleep(75)
  }
  for (let col = 0; col < width; col++){
    element = get_element(row, col)
    element.removeAttribute("class");
  }
}

async function move_down(start_row) {
  for (let row = start_row; row > 1; row--){
    empty_items = 0
    for (let col = 0; col < width; col++){
      current_item = get_element(row, col)
      id = row + '_' + col
      prev_item = get_element((row-1), col)
      current_item.classList = prev_item.classList
      prev_item.removeAttribute("class")
    }
  }
}

async function remove_current_class() {
  var items = document.getElementsByClassName("current")
  items = Array.from(items)
  for (let item_id = 0; item_id < 4; item_id++) {
    try{
      items[item_id].classList.remove("current")
    } catch { }
  }
}

async function can_move_y() {
  try{
    for (let item_id = 3; item_id > -1; item_id--) {
      item = items[item_id]
      id = item.id

      next_id = (parseInt(id.split('_')[0]) + 1) + '_' + id.split('_')[1]
      var next_item = document.getElementById(next_id)
      try {
        if (next_item.classList.contains("filled") &&       !next_item.classList.contains("current")) {return false}
      } catch {
        // await check_rows(length);
        remove_current_class();}
    }
    return true
  } catch {return false}
}

function can_move_left(){
  var items = document.getElementsByClassName("current")
  for (let item_id = 0; item_id < 4; item_id++) {
    current_item = items[item_id]
    row = current_item.id.split('_')[0]
    col = parseInt(current_item.id.split('_')[1])
    if (col == 0){
      return false
    }
    next_id = (row + '_' + (col - 1))
    next_item = document.getElementById(next_id)
    if (!next_item.classList.contains("current")){
      if (current_item.classList.contains("current") && next_item.classList.contains("filled")) { return false }
    }
  }
  return true
}

async function move_left() {
  if (can_move_left()){
    for (let row = 0; row <= length; row++){
      next_item = get_element(row, 0)
      for (let col = 1; col < width; col++) {
        current_item = get_element(row, col)
        if (current_item.classList.contains("current")){
          next_item.classList = current_item.classList
          current_item.removeAttribute("class")
        }
        next_item = current_item
      }
    }
  }
}

function can_move_right(){
  var items = document.getElementsByClassName("current")
  for (let item_id = 0; item_id < 4; item_id++) {
    current_item = items[item_id]
    row = current_item.id.split('_')[0]
    col = parseInt(current_item.id.split('_')[1])
    if (col == parseInt(width-1)){
      return false
    }
    next_id = (row + '_' + (col + 1))
    next_item = document.getElementById(next_id)
    if (!next_item.classList.contains("current")){
      if (current_item.classList.contains("current") && next_item.classList.contains("filled")) { return false }
    }
  }
  return true
}

async function move_right() {
  if (can_move_right()){
    for (let row = 0; row <= length; row++){
      next_item = get_element(row, width-1)
      for (let col = width-2; col > -1; col--) {
        current_item = get_element(row, col)
        if (current_item.classList.contains("current")){
            next_item.classList = current_item.classList
            current_item.removeAttribute("class")
        }
        next_item = current_item
      }
    }
  }
}

function checkKeyMove() {
  if (!lost){
    if (keyState[37]) {
      move_left()
    }
    else if (keyState[39]) {
      move_right()
    }
    setTimeout(checkKeyMove, 100);
  }
}

function dimm_tables(){
  tables = document.getElementsByTagName("table")
  for (let i = 0; i < 2; i++){
    tables[i].classList.toggle("table-dimmed")
  }
}

function undimm_tables(){
  tables = document.getElementsByTagName("table")
  for (let i = 0; i < 2; i++){
    tables[i].classList.remove("table-dimmed")
  }
}

async function game_over(){

  for (let col = 0; col < width; col++){
    id = "3_" + col
    if (document.getElementById(id).classList.contains("filled")){
      document.getElementById('id_score').value = parseInt(document.getElementById('score').innerHTML);
      console.log('score: ', score);
      console.log(document.getElementById('id_score'))
      lost = true
      dimm_tables()
      position_sign()
      game_over_sign.style.opacity = 1;
      document.getElementById('save_score_btn').click();
      return null;
    }
  }
}
function position_sign(){
  game_over_sign = document.getElementsByClassName("game-over")[0]
  middle_cell = document.getElementById("8_3")
  rect = middle_cell.getBoundingClientRect();
  game_over_sign.style.top = (rect.top + window.scrollY + 1).toString() + "px";
  game_over_sign.style.left = (rect.left - 59.5).toString() + "px";

  middle_cell = document.getElementById("10_3")
  rect = middle_cell.getBoundingClientRect();
  score_saved_sign.style.top = (rect.top + window.scrollY + 1).toString() + "px";
  score_saved_sign.style.left = (rect.left - 59.5).toString() + "px";
}

function initiate(){
  hide_upper_rows()
  window.addEventListener('keydown', async function(e){
      keyState[e.keyCode || e.which] = true;
      if (!lost){
        if (e.keyCode == "27") {
          // alert('game paused')
          dimm_tables();
          if (game_paused) {
            await sleep(current_speed * 5)
          }
          game_paused = game_paused ? false : true
        }
        else if (e.keyCode == "38") {
          rotate()
        }
      }
  },true);
  window.addEventListener('keyup',function(e){
      keyState[e.keyCode || e.which] = false;
  },true);
}

function hide_upper_rows(){
  for (let row = 0; row < 4; row++){
    for (let col = 0; col < width; col++){
      id =  row + '_' + col
      item = document.getElementById(id)
      item.style.display = "none"
    }
  }
}

function reset(){
  try{
    game_over_sign.style.opacity = 0
    undimm_tables()
  } catch {}
  score = 0
  game_paused = false
  score_element.innerHTML = 0
  lost = true
  for (let row = 0; row < length+1; row++){
    for (let col = 0; col < width; col++){
      element = get_element(row, col)
      element.removeAttribute("class")
    }
  }
  for (let row = 0; row < 5; row++){
    for (let col = 1; col < 6; col++){
      row_id = 'sub' + row
      element = get_element(row_id, col)
      element.removeAttribute("class")
    }
  }
}

async function game() {
  if (lost == false){return null}
  reset()
  if (speed == 80){
    choose_difficulty("normal")
  }
  lost = false
  generate_next_object()
  checkKeyMove()
  score = 0
  score_saved_sign.style.animationName = "";
  document.getElementById('id_score').value = 0;
  current_speed = speed
  while (!lost){
    await spawn_object()
    await sleep(500)
    await move_object()
    await remove_current_class()
    await game_over()
  }
  window.removeEventListener("keydown", checkKeyMove, false);
}

document.onkeydown = KD;
       function KD(e) {
         if ([37, 38, 39, 40].includes(e.keyCode)){
           event.returnValue = false;
         }
       }

window.addEventListener('resize', position_sign)

$(document).on('submit', '#post_score_form', function(e){
  e.preventDefault();
  if ((score > 0) && (lost == true)){
    score_saved_sign.style.animationName = "opacityOnAndOff";
    $.ajax({
      method:'POST',
      url: 'api/add-post',
      data: {
        score: document.getElementById('id_score').value,
        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
      },
    });
  }
});

initiate()
