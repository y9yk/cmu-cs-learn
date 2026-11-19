const {test}=require('node:test');
const assert=require('node:assert/strict');
const {matches,normalize}=require('../docs/study.js');
const c={keywords:'11-768 AI Agents 인공지능 에이전트 평가 모델',track:'agents',status:'available',id:'11-768'};
test('교과목 번호 표기 차이를 허용한다',()=>assert.equal(matches(c,{q:'１１ ７６８',track:'all'}),true));
test('한국어·영어 검색어를 함께 찾는다',()=>assert.equal(matches(c,{q:'agents 평가',track:'all'}),true));
test('검색어는 모두 존재해야 한다',()=>assert.equal(matches(c,{q:'agents 멀티모달',track:'all'}),false));
test('주제와 공개 상태를 동시에 필터한다',()=>{
 assert.equal(matches(c,{q:'',track:'agents',status:'available'}),true);
 assert.equal(matches(c,{q:'',track:'software',status:'available'}),false);
 assert.equal(matches(c,{q:'',track:'agents',status:'planned'}),false);
});
test('완료 과목을 실제 저장 상태로 거른다',()=>{
 assert.equal(matches(c,{q:'agents',track:'all',progress:'done',seen:new Set(['11-768'])}),true);
 assert.equal(matches(c,{q:'agents',track:'all',progress:'done',seen:new Set()}),false);
 assert.equal(matches(c,{q:'agents',track:'all',progress:'open',seen:new Set(['11-768'])}),false);
});
test('한글 조합 및 하이픈을 정규화한다',()=>assert.equal(normalize('한글–A   B'),'한글 a b'));
