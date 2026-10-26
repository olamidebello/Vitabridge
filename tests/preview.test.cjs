const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const nodes={};function node(s){return nodes[s]||(nodes[s]={value:s==='#role'?'Dispatcher':'',style:{},innerHTML:'',textContent:'',append(){},setAttribute(){},showModal(){},close(){},insertAdjacentHTML(){},parentNode:{insertBefore(){}}})}
const c={document:{querySelector:node,createElement:()=>node('option')},navigator:{},window:{addEventListener(){}},structuredClone,setTimeout(){},URL,console,FormData:class{constructor(target){return target.data}}};vm.createContext(c);for(const f of ['app.js','admin.js'])vm.runInContext(fs.readFileSync('dist/'+f,'utf8'),c);
vm.runInContext(`
$('#role').value='Super admin';
function check(ok,msg){if(!ok)throw Error(msg)}
let originalName=products[0].name;credits=500;saveTenantState();switchTenant('tenant-2');check(trips.length===0&&products.length===0&&credits===0,'new tenant must be empty');products.push({id:'second',name:'Second org',price:500,currency:'USD',active:true});switchTenant('tenant-1');check(products[0].name===originalName&&credits===500,'tenant restore failed');check(!products.some(p=>p.id==='second'),'cross-tenant product leak');
gateways.Stripe.enabled=true;placeOrder({preventDefault(){},target:{gateway:{value:'Stripe'}}},'prod-1');check(orders.length===1&&orders[0].status==='Simulated — unpaid','demo order invalid');let price=orders[0].amount;products[0].price=99999;check(orders[0].amount===price,'order snapshot changed');
currentTenant().status='Suspended';placeOrder({preventDefault(){},target:{gateway:{value:'Stripe'}}},'prod-1');check(orders.length===1,'suspended tenant created order');currentTenant().status='Active';features.marketplace=false;placeOrder({preventDefault(){},target:{gateway:{value:'Stripe'}}},'prod-1');check(orders.length===1,'disabled marketplace created order');
switchTenant('tenant-2');check(orders.length===0,'order crossed tenant boundary');
`,c);console.log('PASS: tenant state separation, restoration, order snapshot, suspension and marketplace gates');
