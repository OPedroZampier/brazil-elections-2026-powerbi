import fs from 'node:fs/promises';
import path from 'node:path';
import {createRequire} from 'node:module';
const require=createRequire('C:/Users/pedro/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/asset.cjs');
const sharp=require('sharp');
const out=process.argv[2];
const pages=[
 ['07-eleitos-qp-segundo-turno','ELEITOS, QP E SEGUNDO TURNO',['ELEITOS POR QP','ELEITOS POR MÉDIA','% PROPORCIONAIS POR QP','CANDIDATOS NO 2º TURNO'],'FORMA DE ELEIÇÃO POR PARTIDO','QP E MÉDIA POR CARGO','CONSULTA DE ELEITOS E SEGUNDO TURNO',true],
 ['08-votacao-primeiro-turno','VOTAÇÃO DO PRIMEIRO TURNO',['VOTOS VÁLIDOS','VOTOS NOMINAIS','VOTOS DE LEGENDA','SEÇÕES TOTALIZADAS'],'VOTAÇÃO POR CANDIDATO','VOTAÇÃO POR UF','DETALHAMENTO DOS RESULTADOS',true],
 ['09-participacao-eleitoral','PARTICIPAÇÃO ELEITORAL',['COMPARECIMENTO','TAXA DE ABSTENÇÃO','VOTOS BRANCOS (%)','VOTOS NULOS (%)'],'ABSTENÇÃO POR UF','COMPOSIÇÃO DOS VOTOS','PARTICIPAÇÃO E COBERTURA POR UF',false]
];
const text=(x,y,t,size=16,color='#b6c8d9',weight=600)=>`<text x="${x}" y="${y}" fill="${color}" font-family="Segoe UI,Arial,sans-serif" font-size="${size}" font-weight="${weight}">${t}</text>`;
const box=(x,y,w,h,title,card=false)=>`<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="9" fill="#0b2239" stroke="#29495f"/>${card?`<path d="M${x},${y}h${w}" stroke="#22c5a4" stroke-width="3"/>`:''}${text(x+20,y+29,title,card?12:16)}${card?'':`<path d="M${x+20},${y+42}h${w-40}" stroke="#244b60"/>`}`;
await fs.mkdir(path.join(out,'fundos'),{recursive:true});
for(const [name,title,cards,left,right,table,filters] of pages){
 let svg=`<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720" viewBox="0 0 1280 720"><defs><radialGradient id="glow"><stop stop-color="#064948"/><stop offset="1" stop-color="#031529"/></radialGradient></defs><rect width="1280" height="720" fill="#031529"/><rect width="1280" height="720" fill="url(#glow)" opacity=".42"/>`;
 for(let i=0;i<9;i++)svg+=`<path d="M${i*120-500},720 L${i*120+240},0" stroke="#14617b" stroke-opacity=".15" fill="none"/>`;
 svg+=`<rect x="32" y="20" width="1216" height="98" fill="#071a2c"/>${text(56,65,'ELEIÇÕES 2026',36,'#f4f7fc',700)}${text(56,97,title,19,'#22c5a4',700)}`;
 for(const [x,w,label] of (filters?[[865,110,'UF'],[985,120,'CARGO'],[1115,112,'PARTIDO']]:[[1115,112,'UF']]))svg+=`<rect x="${x}" y="38" width="${w}" height="62" rx="5" stroke="#22c5a4" fill="#0b2239"/>${text(x+12,57,label,11)}`;
 cards.forEach((label,i)=>{svg+=box(40+i*304,140,288,110,label,true);});
 svg+=box(40,270,744,232,left)+box(800,270,440,232,right)+box(40,520,1200,142,table);
 svg+=`<path d="M40 675H1240" stroke="#b99839" stroke-width="1"/>${text(40,701,'Fonte: Tribunal Superior Eleitoral',11,'#8ba4b7',400)}${text(948,701,'Primeiro turno · Eleições 2026',11,'#8ba4b7',400)}</svg>`;
 await fs.writeFile(path.join(out,'fundos',name+'.svg'),svg);
 await sharp(Buffer.from(svg)).png().toFile(path.join(out,'fundos',name+'.png'));
}
console.log('3 fundos SVG e PNG gerados em 1280 × 720.');
