use tpc07;

create table if not exists EUTOAQUI(
	JotaPe int primary key
);

create table if not exists cliente(
	codcliente INT primary key auto_increment,
    nome VARCHAR(40),
    endereco VARCHAR(100)
);

create table if not exists produto(
	codproduto INT primary key auto_increment,
    descricao VARCHAR(50),
    preco DECIMAL(8,2)
);

create table if not exists venda(
	codvenda INT primary key auto_increment,
    data DATE,
    valor_total DECIMAL(8,2),
    codcliente INT,
    foreign key(codcliente) references cliente(codcliente)
);

create table if not exists item_venda(
	codvenda INT,
    codproduto INT,
    qtde INT,
    valor DECIMAL(8,2),
    primary key(codvenda, codproduto),
    foreign key(codvenda) references venda(codvenda),
    foreign key(codproduto) references produto(codproduto)
);	