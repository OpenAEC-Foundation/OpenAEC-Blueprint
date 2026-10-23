import assert from 'node:assert/strict';
function buildPattern(query, matchCase, wholeWord) {
  const searchQuery = matchCase ? query : query.toLowerCase();
  const wordBoundary = wholeWord ? '\\b' : '';
  const escapedQuery = searchQuery.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  return new RegExp(wordBoundary + escapedQuery + wordBoundary, matchCase ? 'g' : 'gi');
}
const cases=[
 {query:'beton',text:'beton',whole:true,expected:1},
 {query:'beton',text:'betonvloer',whole:true,expected:0},
 {query:'één',text:'één',whole:true,expected:0},
 {query:'één',text:'één',whole:false,expected:1},
 {query:'beton',text:'cafébeton',whole:true,expected:1},
 {query:'café',text:'café',whole:true,expected:0},
];
for(const row of cases){row.actual=[...row.text.matchAll(buildPattern(row.query,false,row.whole))].length;assert.equal(row.actual,row.expected);}
process.stdout.write(JSON.stringify({cases,assertions:cases.length},null,2));
