let config = {
    type: Phaser.AUTO,
    width: 800,
    height: 600,
    physics: {
        default: 'arcade',
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
let starCount = 0;
let progress;
let canvas;
let question_count = 0;
let answers = [];
let announcement;

// Example data from the database
let question_db = [
    {'id': 0,
    'chapter': 1,
    'text': "Quoi est-elle la capitale de la France ?"},
    {'id': 1,
    'chapter': 1,
    'text': "Quoi est-elle la capitale des Etats-Unis ?"},
    {'id': 2,
    'chapter': 1,
    'text': "Quoi est-elle la capitale de la Lithuanie ?"},
];
let answer_db = [
    {'id': 1,
    'q_id': 0,
    'text': 'Pas de Calais',
    'correct': false},
    {'id': 2,
    'q_id': 0,
    'text': 'Marseille',
    'correct': false},
    {'id': 3,
    'q_id': 0,
    'text': 'Paris',
    'correct': true},
    {'id': 4,
    'q_id': 1,
    'text': 'New York City',
    'correct': false},
    {'id': 5,
    'q_id': 1,
    'text': 'Washington, D.C.',
    'correct': true},
    {'id': 6,
    'q_id': 1,
    'text': 'Little Rock',
    'correct': false},
    {'id': 7,
    'q_id': 2,
    'text': 'Riga',
    'correct': false},
    {'id': 8,
    'q_id': 2,
    'text': 'Vilnius',
    'correct': true},
    {'id': 9,
    'q_id': 2,
    'text': 'Kalingrad',
    'correct': false}
];

// Creation de l'objet
let game = new Phaser.Game(config);

// Chargement des images et des sprites
function preload () {
    this.load.image('sky', './assets/sky.png');
    this.load.image('ground', './assets/platform.png');
    this.load.image('star', './assets/star.png');
    this.load.image('bomb', './assets/bomb.png');
    this.load.spritesheet('dude', './assets/dude.png', { frameWidth: 32, frameHeight: 48 });
}

// Creations des objets du jeu
function create () {
    // Background
    this.add.image(400, 300, 'sky');

    // Creation d'un objet platform
    platforms = this.physics.add.staticGroup();

    // Creation d'une platform et resize en 2
    platforms.create(400, 568, 'ground').setScale(2).refreshBody();

    // Creation de 3 platform
    platforms.create(600, 400, 'ground');
    platforms.create(50, 250, 'ground');
    platforms.create(750, 220, 'ground');

    // Creation d'un objet player
    player = this.physics.add.sprite(100, 450, 'dude');

    // Attribution d'une propriete de rebond et collision avec les bords de l'ecran
    player.setBounce(0.2);
    player.setCollideWorldBounds(true);

    // Creation des animations de mouvement (gauche, droite, arret)
    this.anims.create({
        key: 'left',
        frames: this.anims.generateFrameNumbers('dude', { start: 0, end: 3 }),
        frameRate: 10,
        repeat: -1
    });

    this.anims.create({
        key: 'turn',
        frames: [ { key: 'dude', frame: 4 } ],
        frameRate: 20
    });

    this.anims.create({
        key: 'right',
        frames: this.anims.generateFrameNumbers('dude', { start: 5, end: 8 }),
        frameRate: 10,
        repeat: -1
    });

    // Input Events
    cursors = this.input.keyboard.createCursorKeys();

    // Creation d'un groupe etoile (creation d'une etoile + 11 autres avec decalage sur l'axe x)
    stars = this.physics.add.group({
        key: 'star',
        repeat: 11,
        setXY: { x: 12, y: 0, stepX: 70 }
    });

    stars.children.iterate(function (child) {
        // Effet de rebond different pour chaque etoile
        child.setBounceY(Phaser.Math.FloatBetween(0.4, 0.8));
    });

    // Creation d'un objet bombe
    bombs = this.physics.add.group();

    // Affichage du score
    scoreText = this.add.text(16, 50, 'Score: 0', { fontSize: '25px', fill: '#000' });

    // Gestion des collisions
    this.physics.add.collider(player, platforms);
    this.physics.add.collider(stars, platforms);
    this.physics.add.collider(bombs, platforms);

    // Si superposition entre le joueur et une etoile, appel de la fonction collectStar
    this.physics.add.overlap(player, stars, collectStar, null, this);

    // Si superposition entre le joueur et une bombe, appel de la fonction hitBomb
    this.physics.add.collider(player, bombs, hitBomb, null, this);

    // Canvas
    canvas = document.getElementsByTagName('canvas')
    canvas = canvas[0]

    // Affichage du progres
    let chapter = "Les Capitales: Niveau 1"; // Pulled from database
    progress = this.add.text(16, 16, chapter, { fontSize: '25px', fill: '#000'})

    // announcement message
    announcement = this.add.text(200, 130, "", { fontSize: '40px', fill: '#000'});
}

// Animation et gestion des evenements
function update () {
    // Si game over, arret de la fonction
    if (gameOver)
    {
        return;
    }

    // Si touche enfoncee
    if (cursors.left.isDown) {
        player.setVelocityX(-160);
        player.anims.play('left', true);
    }
    else if (cursors.right.isDown) {
        player.setVelocityX(160);
        player.anims.play('right', true);
    }
    else {
        player.setVelocityX(0);
        player.anims.play('turn');
    }

    // Verification du contact avec le sol pour le saut
    if (cursors.up.isDown && player.body.touching.down) {
        player.setVelocityY(-530);
    }
}

function collectStar (player, star) {
    // Suppression de l'etoile
    star.disableBody(true, true);

    // Mise a jour du score
    score += 10;
    scoreText.setText('Score: ' + score);

    starCount += 1;

    // Si toutes les etoiles sont collectees
    if (stars.countActive(true) === 0) {
        // Generation de nouvelles etoiles
        stars.children.iterate(function (child) {
            child.enableBody(true, child.x, 0, true, true);
        });

        // Creation de la bombe a une hauteur aleatoire mais toujours a l'oppose du joueur
        let x = (player.x < 400) ? Phaser.Math.Between(400, 800) : Phaser.Math.Between(0, 400);

        // Creation d'une bombe
        let bomb = bombs.create(x, 16, 'bomb');
        bomb.setBounce(1);
        bomb.setCollideWorldBounds(true);
        bomb.setVelocity(Phaser.Math.Between(-200, 200), 20);
        // Suppression de la gravite
        bomb.allowGravity = false;
    }
    // Si il y a des questions qui restent a poser
    else if (question_count < question_db.length) {
        // Une question est posee apres 3 etoiles attrappees
        if (starCount % 3 === 0) {
            announcement.setText('')
            this.physics.pause()

            let questionID = question_db[question_count].id;

            // Une question choisie par le parametre question_count
            question = this.add.text(120, 100, question_db[question_count].text, { fontSize: '25px', fill: '#000'})

            // Generation d'une liste des reponses qui correspondent a la question
            let y_position = 130;
            answers = []
            answer_db.forEach(obj => {
                if (obj.q_id === questionID) {
                    answers.push({
                        database: obj,
                        shown: this.add.text(150, y_position, obj.text, { fontSize: '20px', fill: '#000'})
                    })
                    y_position += 25
                }
            })
            console.log(answers)
            // Selection d'une reponse
            chooseResponse(answers, this)
        }
    }
}

function hitBomb (player, bomb) {
    this.physics.pause();
    player.setTint(0xff0000);
    player.anims.play('turn');
    gameOver = true;
}

function chooseResponse (answers, my_this) {
    // Attend que l'utilisateur click
    canvas.onclick = (e) => {
        let responseChosen = false
        let count = 0

        // Compare les coordonnees des objets contre celles du click
        while (count < answers.length) {
            let x_c = answers[count].shown.x
            let y_c = answers[count].shown.y
            let w = answers[count].shown.width
            let h = answers[count].shown.height + 70 // Il faut ajouter 70 px pour une raison....

            if (e.clientX >= x_c && e.clientX <= x_c + w) {
                if (e.clientY >= y_c && e.clientY <= y_c + h) {
                    responseChosen = true
                    break
                }
            }
            count += 1
        }
        if (responseChosen) {
            console.log("Reponse choisie: ", answers[count].database.text)
            // Faire dispairaitre la question et ses reponses
            answers[0].shown.setText('')
            answers[1].shown.setText('')
            answers[2].shown.setText('')
            question.text = ''
            if (answers[count].database.correct) {
                announcement.setText("Tres bien!\n+10 points")
                score += 10
                scoreText.setText('Score: ' + score);
            } else {
                announcement.setText('Mauvaise reponse!\n-5 points')
                score -= 5
                scoreText.setText('Score: ' + score);
            }
            // Avance a la prochaine question
            question_count += 1
            my_this.physics.resume()
        }
    }
}