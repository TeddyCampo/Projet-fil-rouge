let config = {
  type: Phaser.AUTO,
  width: 800,
  height: 600,
  parent: "phaser-game",
  physics: {
    default: "arcade",
    arcade: {
      gravity: { y: 600 },
      debug: false
    }
  },
  scene: {
    preload: preload,
    create: create,
    update: update
  }
};

// Variables globales
let player;
let stars;
let bombs;
let platforms;
let cursors;
let score = 0;
let gameOver = false;
let scoreText;
let question;
let q_and_a;
let theme_title;
let starCount = 0;
let progress;
let canvas;
let questionCount = 0;
let answers = [];
let arrows = [];
let announcement;
let questionnaire;
let validate;
let index = 0;
let down_is_down;
let up_is_down;

// AJAX Request for user and score from database
function get_and_show_score(instance) {
  $(function() {
    $.ajax({
      url: "/get_score/",
      type: "GET",
      dataType: "json"
      /* AJAX request call the view "get_score" which send back a json object from the database*/
    }).done(function(response) {
      console.log(response.score);
      /* The json object sent by the view has a "score" property with a value.*/
      score = response.score;
      /* Store the score in a new variable scoreText to display it in the game window. */
      scoreText = instance.add.text(16, 50, "Score: " + score, {
        fontSize: "25px",
        fill: "#000"
      });
    });
  });
  return score;
}

// AJAX Request for questions and answers from database
function get_q_and_a(instance) {
  $(function() {
    $.ajax({
      url: "/get_q_and_a/",
      type: "GET",
      dataType: "json"
      /* AJAX request call the view "get_score" which send back a json object from the database*/
    }).done(function(response) {
      console.log(response);
      q_and_a = response;
      question_db = q_and_a.questions;
      answer_db = q_and_a.answers;
      theme_title = q_and_a.theme.themeName;

      // Affichage du progres
      progress = instance.add.text(16, 16, theme_title, {
        fontSize: "25px",
        fill: "#000"
      });
    });
  });
}

// Get cookie so that CSRF token can be made later for Post request
function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
      var cookie = jQuery.trim(cookies[i]);
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// AJAX Post request for sending score to database
function send_score(score) {
  var csrf_token = getCookie("csrftoken");

  console.log(csrf_token);
  $(function() {
    $.ajax({
      url: "/update_score/",
      content: "application/x-www-form-urlencoded",
      data: { csrfmiddlewaretoken: csrf_token, score: score },
      type: "POST"
    }).done(function(response) {
      console.log(response);
    });
  });
}

function get_next_theme() {
  finishedTheme = q_and_a.theme.id;
  $(function() {
    $.ajax({
      url: `/get_next_theme?theme=${finishedTheme}`,
      type: "GET",
      dataType: "json"
      /* AJAX request call the view "get_score" which send back a json object from the database*/
    }).done(function(response) {
      console.log(response);
      q_and_a = response;
      question_db = q_and_a.questions;
      answer_db = q_and_a.answers;
      theme_title = q_and_a.theme.themeName;

      // Affichage du progres
      progress.setText(theme_title);
    });
  });
}

// Creation de l'objet
let game = new Phaser.Game(config);

// Chargement des images et des sprites
function preload() {
  this.load.image("sky", "./static/assets/images/sky.png");
  this.load.image("ground", "./static/assets/images/platform.png");
  this.load.image("star", "./static/assets/images/star.png");
  this.load.image("bomb", "./static/assets/images/bomb.png");
  this.load.spritesheet("dude", "./static/assets/images/dude.png", {
    frameWidth: 32,
    frameHeight: 48
  });
}

// Creations des objets du jeu
function create() {
  // Background
  this.add.image(400, 300, "sky");

  // Creation d'un objet platform
  platforms = this.physics.add.staticGroup();

  // Creation d'une platform et resize en 2
  platforms
    .create(400, 568, "ground")
    .setScale(2)
    .refreshBody();

  // Creation de 3 platform
  platforms.create(600, 400, "ground");
  platforms.create(50, 250, "ground");
  platforms.create(750, 220, "ground");

  // Creation d'un objet player
  player = this.physics.add.sprite(100, 450, "dude");

  // Attribution d'une propriete de rebond et collision avec les bords de l'ecran
  player.setBounce(0.2);
  player.setCollideWorldBounds(true);

  // Creation des animations de mouvement (gauche, droite, arret)
  this.anims.create({
    key: "left",
    frames: this.anims.generateFrameNumbers("dude", { start: 0, end: 3 }),
    frameRate: 10,
    repeat: -1
  });

  this.anims.create({
    key: "turn",
    frames: [{ key: "dude", frame: 4 }],
    frameRate: 20
  });

  this.anims.create({
    key: "right",
    frames: this.anims.generateFrameNumbers("dude", { start: 5, end: 8 }),
    frameRate: 10,
    repeat: -1
  });

  // Input Events
  cursors = this.input.keyboard.createCursorKeys();

  // Pour valider l'une des reponses, l'utilisateur utilise le cle entre
  validate = this.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.ENTER);

  // Creation d'un groupe etoile (creation d'une etoile + 11 autres avec decalage sur l'axe x)
  stars = this.physics.add.group({
    key: "star",
    repeat: 11,
    setXY: { x: 12, y: 0, stepX: 70 }
  });

  stars.children.iterate(function(child) {
    // Effet de rebond different pour chaque etoile
    child.setBounceY(Phaser.Math.FloatBetween(0.4, 0.8));
  });

  // Creation d'un objet bombe
  bombs = this.physics.add.group();

  // Affichage du score
  score = get_and_show_score(this);

  // Get questions, answers, theme and display theme
  get_q_and_a(this);

  // Gestion des collisions
  this.physics.add.collider(player, platforms);
  this.physics.add.collider(stars, platforms);
  this.physics.add.collider(bombs, platforms);

  // Si superposition entre le joueur et une etoile, appel de la fonction collectStar
  this.physics.add.overlap(player, stars, collectStar, null, this);

  // Si superposition entre le joueur et une bombe, appel de la fonction hitBomb
  this.physics.add.collider(player, bombs, hitBomb, null, this);

  // Canvas
  canvas = document.getElementsByTagName("canvas");
  canvas = canvas[0];

  // announcement message
  announcement = this.add.text(200, 130, "", {
    fontSize: "40px",
    fill: "#000"
  });
}

// Animation et gestion des evenements
function update() {
  // Si game over, arret de la fonction
  if (gameOver) {
    return;
  }

  // Si les questions sont affichees
  if (questionnaire) {
    arrows[index].setText("> ");

    if (cursors.left.isDown || cursors.right.isDown) {
      down_is_down = false;
      up_is_down = false;
    } else if (cursors.down.isDown) {
      down_is_down = true;
      up_is_down = false;
    } else if (cursors.up.isDown) {
      up_is_down = true;
      down_is_down = false;
    } else if (down_is_down && cursors.down.isUp) {
      down_is_down = false;
      arrows[index].setText("");
      index = (index + 1) % arrows.length;
      console.log(index);
    } else if (up_is_down && cursors.up.isUp) {
      up_is_down = false;
      arrows[index].setText("");
      index = (index + (arrows.length - 1)) % arrows.length;
      console.log(index);
    } else if (validate.isDown) {
      arrows[index].setText("");
      timer = 0;
      // Passe les parametres pour traiter le choix
      userChose(answers, index, this);
    }
  }
  // Si touche enfoncee pendant le jeux normal
  else {
    if (cursors.left.isDown) {
      player.setVelocityX(-160);
      player.anims.play("left", true);
    } else if (cursors.right.isDown) {
      player.setVelocityX(160);
      player.anims.play("right", true);
    } else {
      player.setVelocityX(0);
      player.anims.play("turn");
    }

    // Verification du contact avec le sol pour le saut
    if (cursors.up.isDown && player.body.touching.down) {
      player.setVelocityY(-530);
    }
  }
}

function collectStar(player, star) {
  // Suppression de l'etoile
  star.disableBody(true, true);

  // Mise a jour du score
  score += 10;
  scoreText.setText("Score: " + score);

  starCount += 1;

  // Si toutes les etoiles sont collectees
  if (stars.countActive(true) === 0) {
    // Generation de nouvelles etoiles
    stars.children.iterate(function(child) {
      child.enableBody(true, child.x, 0, true, true);
    });
  }
  // Affiche la question est ses reponses
  else if (starCount % 3 === 0) {
    announcement.setText("");
    this.physics.pause();

    let questionID = question_db[questionCount].id;

    // Une question choisie par le parametre questionCount
    question = this.add.text(
      120,
      100,
      question_db[questionCount].questionText,
      {
        fontSize: "25px",
        fill: "#000"
      }
    );

    // Generation d'une liste des reponses qui correspondent a la question
    let y_position = 130;
    answers = [];
    answer_db.forEach(obj => {
      if (obj.question === questionID) {
        answers.push({
          database: obj,
          shown: this.add.text(150, y_position, obj.answerText, {
            fontSize: "20px",
            fill: "#000"
          })
        });
        arrows.push(
          this.add.text(120, y_position, "", { fontSize: "20px", fill: "#000" })
        );
        y_position += 25;
      }
    });
    console.log("Answers: ", answers);
    questionnaire = true;
  }
}

function hitBomb(player, bomb) {
  this.physics.pause();
  player.setTint(0xff0000);
  player.anims.play("turn");
  announcement.setText("Dommage, tu es mort");

  send_score(score);

  gameOver = true;
}

// Deconstruction de la questionnaire
function userChose(answers, count, my_this) {
  answers[0].shown.setText("");
  answers[1].shown.setText("");
  answers[2].shown.setText("");
  question.text = "";
  if (answers[count].database.isCorrect) {
    score += 10;
    scoreText.setText("Score: " + score);
    questionCount += 1;

    if (questionCount === question_db.length) {
      my_this.scene.pause();
      send_score(score);
      get_next_theme();
      reset_game(my_this);
    } else {
      announcement.setText("Tres bien!\n+10 points");
    }
  } else {
    announcement.setText("Mauvaise reponse!\n-35 points");
    score -= 35;
    scoreText.setText("Score: " + score);
    questionCount = 0;

    // Creation de la bombe a une hauteur aleatoire mais toujours a l'oppose du joueur
    let x =
      player.x < 400
        ? Phaser.Math.Between(400, 800)
        : Phaser.Math.Between(0, 400);
    // Creation d'une bombe
    let bomb = bombs.create(x, 16, "bomb");
    bomb.setBounce(1);
    bomb.setCollideWorldBounds(true);
    bomb.setVelocity(Phaser.Math.Between(-200, 200), 20);
    // Suppression de la gravite
    bomb.allowGravity = false;
  }
  index = 0;
  questionnaire = null;
  arrows[index].setText("");
  my_this.physics.resume();
}

function reset_game(instance) {
  // Unpause game
  instance.scene.resume();

  // Reset position of player
  player.x = 100;
  player.y = 450;
  questionCount = 0;

  // Erase stars
  stars.children.iterate(child => child.disableBody(true, true));

  // Creation of stars
  stars.children.iterate(function(child) {
    child.enableBody(true, child.x, 0, true, true);
  });

  // Announcing the next level
  announcement.setText("Prochain niveau atteint !");
}
