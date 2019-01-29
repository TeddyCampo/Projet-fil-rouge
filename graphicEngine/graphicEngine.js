import {Phaser} from 'https://cdn.jsdelivr.net/npm/phaser@3.11.0/dist/phaser.js'

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

// Creation de l'objet
let game = new Phaser.Game(config);

// Chargement des images et des sprites
function preload () {
    this.load.image('sky', 'assets/sky.png');
    this.load.image('ground', 'assets/platform.png');
    this.load.image('star', 'assets/star.png');
    this.load.image('bomb', 'assets/bomb.png');
    this.load.spritesheet('dude', 'assets/dude.png', { frameWidth: 32, frameHeight: 48 });
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
    scoreText = this.add.text(16, 16, 'score: 0', { fontSize: '32px', fill: '#000' });

    // Gestion des collisions
    this.physics.add.collider(player, platforms);
    this.physics.add.collider(stars, platforms);
    this.physics.add.collider(bombs, platforms);

    // Si superposition entre le joueur et une etoile, appel de la fonction collectStar
    this.physics.add.overlap(player, stars, collectStar, null, this);

    // Si superposition entre le joueur et une bombe, appel de la fonction hitBomb
    this.physics.add.collider(player, bombs, hitBomb, null, this);
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
}

function hitBomb (player, bomb) {
    this.physics.pause();
    player.setTint(0xff0000);
    player.anims.play('turn');
    gameOver = true;
}