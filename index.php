<!DOCTYPE html>
<html lang="pt">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Ines Osteopata</title>
<link href='https://fonts.googleapis.com/css?family=Jost' rel='stylesheet'>


<style>
html, body { margin: 0; padding: 0; width: 100%; overflow-x: hidden; }
body { font-family: 'Jost', sans-serif; color: #333; }
.logo { height: 50px; }

#imagelanding .int { background: rgba(0,0,0,0.4); }
#imagelanding .int * { color: white; }
#imagelanding .int h1 { font-size: 50px; }
#imagelanding .int h3 { font-size: 25px; }
#imagelanding #knowmore { 
    margin-top: 40px; 
    border: 2px solid white; 
    background: none; 
    padding: 10px 20px; 
    font-size: 25px; 
    color: white; 
    cursor: pointer; 
    transition: background 0.3s ease; 
}
#imagelanding #knowmore:hover { background: rgba(255,255,255,0.2); }

.threecolumncontainer { 
    width: 100vw; 
    position: relative; 
    text-align: center; 
    padding: 40px 0; 
    background: #f8f8f8; 
}
.columnimagecontainer { 
    width: 100%; 
    height: 300px; 
    overflow: hidden; 
    position: relative; 
    background-size: cover; 
    background-position: center top; 
    background-repeat: no-repeat; 
}
.column h2 { 
    margin-top: 30px; 
    font-size: 24px; 
    color: #2c3e50; 
}
.column p { 
    margin-top: 20px; 
    font-size: 16px; 
    color: #555; 
    line-height: 1.6; 
}

/* Contact Section */
#contact { 
    clear: both; 
    background: #2c3e50; 
    color: white; 
    padding: 60px 20px; 
    text-align: center; 
}
#contact h2 { 
    font-size: 32px; 
    margin-bottom: 40px; 
    font-weight: 400; 
}
.contact-container { 
    display: flex; 
    flex-wrap: wrap; 
    justify-content: center; 
    gap: 30px; 
}
.contact-card { 
    background: #34495e; 
    padding: 20px; 
    border-radius: 8px; 
    width: 280px; 
    transition: transform 0.3s ease, box-shadow 0.3s ease; 
}
.contact-card:hover { 
    transform: translateY(-5px); 
    box-shadow: 0 4px 15px rgba(0,0,0,0.3); 
}
.contact-card h3 { 
    font-size: 22px; 
    margin-bottom: 15px; 
}
.contact-card p { 
    font-size: 16px; 
    margin-bottom: 20px; 
    color: #ecf0f1; 
}
.contact-card a { 
    display: inline-block; 
    padding: 10px 20px; 
    background: #3498db; 
    color: white; 
    text-decoration: none; 
    border-radius: 5px; 
    font-size: 16px; 
    transition: background 0.3s ease; 
}
.contact-card a:hover { 
    background: #2980b9; 
}

/* Footer */
footer { 
    background: #1a252f; 
    color: #ecf0f1; 
    text-align: center; 
    padding: 20px; 
    font-size: 14px; 
}

/* Responsive Design */
@media only screen and (max-width: 800px) { 
    .int { 
        padding: 20px; 
        width: 100%; 
        height: 100%; 
        display: table-cell; 
        vertical-align: middle; 
        text-align: center; 
    }
    #title { 
        display: table; 
        width: 100%; 
        height: 50px; 
        position: relative; 
    }
    #imagelanding { 
        display: table; 
        width: 100%; 
        height: calc(100vh - 80px); 
        position: relative; 
        float: right; 
        background: url(assets/images/pexels-yankrukov-5794027.jpg); 
        background-size: cover; 
        background-position: top center; 
    }
    .column { 
        width: 80%; 
        margin: 10%; 
        position: relative; 
        display: inline-block; 
        min-height: 50vh; 
        vertical-align: top; 
    }
    #title .int h3 { font-size: 25px; }
    #contact h2 { font-size: 28px; }
    .contact-card { width: 100%; max-width: 300px; }
}

@media only screen and (min-width: 801px) {
    .int { 
        padding: 20px; 
        width: 100%; 
        height: 100%; 
        display: table-cell; 
        vertical-align: middle; 
        text-align: center; 
    }
    #title { 
        display: table; 
        width: 30%; 
        height: 100vh; 
        position: relative; 
        float: left; 
    }
    #imagelanding { 
        display: table; 
        width: 70%; 
        height: 100vh; 
        position: relative; 
        float: right; 
        background: url(assets/images/pexels-yankrukov-5794027.jpg); 
        background-size: cover; 
        background-position: top center; 
    }
    #title .int h3 { font-size: 35px; }
    .column { 
        width: calc(100% / 4); 
        margin: 0 1.5%; 
        position: relative; 
        display: inline-block; 
        min-height: 80vh; 
        vertical-align: top; 
    }
    #contact h2 { font-size: 32px; }
    .contact-card { width: 280px; }
}
</style>
</head>
<body>
<div id="title">
    <div class="int">
        <h3><img class="logo" src="assets/images/ineslogo.png"> Ines Osteopata</h3>
    </div>
</div>

<div id="imagelanding">
    <div class="int">
        <h1>Cuidados de Saúde Personalizados</h1>
        <h3>Saúde e bem-estar para uma vida equilibrada.</h3>
        <button id="knowmore">Saiba Mais</button>
    </div>
</div>

<div style="clear: both; padding: 40px; text-align: center;">
    <h3>Sobre Ines Osteopata</h3>
</div ..

<div class="threecolumncontainer">
    <div class="column">
        <div class="columnimagecontainer" style="background-image: url(assets/images/mission.jpg);"></div>
        <h2>Nossa Missão</h2>
        <p>Na Ines Osteopata, a nossa missão é promover a saúde e o bem-estar da nossa comunidade. Acreditamos que a educação em saúde é fundamental para ajudar as pessoas a tomarem decisões informadas sobre o seu estilo de vida.</p>
    </div>
    <div class="column">
        <div class="columnimagecontainer" style="background-image: url(assets/images/services.jpg);"></div>
        <h2>Nossos Serviços</h2>
        <p>Oferecemos uma variedade de serviços de saúde, incluindo consultas, workshops de bem-estar e programas de nutrição personalizados. Cada serviço é projetado para atender às necessidades individuais dos nossos clientes, garantindo uma abordagem holística para a saúde.</p>
    </div>
    <div class="column">
        <div class="columnimagecontainer" style="background-image: url(assets/images/team.jpg);"></div>
        <h2>Equipe Especializada</h2>
        <p>A nossa equipe é composta por profissionais de saúde altamente qualificados e experientes. Estamos comprometidos em fornecer cuidados de qualidade e apoio contínuo, ajudando os nossos clientes a atingirem os seus objetivos de saúde.</p>
    </div>
</div>

<div id="contact">
    <h3><img class="logo" src="assets/images/ineslogo.png"> Ines Osteopata</h3>
    <h2>Entre em Contato</h2>
    <div class="contact-container">
        <div class="contact-card">
            <h3>Clínica Lisboa</h3>
            <p>Visite nossa clínica em Lisboa para cuidados personalizados.</p>
            <a href="https://lisboa.inesosteopata.pt">Saiba Mais</a>
        </div>
        <div class="contact-card">
            <h3>Clínica Porto</h3>
            <p>Conheça nossa equipe no Porto para serviços de bem-estar.</p>
            <a href="https://porto.inesosteopata.pt">Saiba Mais</a>
        </div>
        <div class="contact-card">
            <h3>Clínica Faro</h3>
            <p>Descubra nossos programas de saúde em Faro.</p>
            <a href="https://faro.inesosteopata.pt">Saiba Mais</a>
        </div>
    </div>
</div>

<footer>
    <p>Made by Vianexu</p>
</footer>
</body>
</html>