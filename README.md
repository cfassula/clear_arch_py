# Pyhton_template
##Conventional commits
test: indica qualquer tipo de criação ou alteração de códigos de teste. Exemplo: Criação de testes unitários.
feat: indica o desenvolvimento de uma nova feature ao projeto. Exemplo: Acréscimo de um serviço, funcionalidade, endpoint, etc.
refactor: usado quando houver uma refatoração de código que não tenha qualquer tipo de impacto na lógica/regras de negócio do sistema. Exemplo: Mudanças de código após um code review
style: empregado quando há mudanças de formatação e estilo do código que não alteram o sistema de nenhuma forma.
Exemplo: Mudar o style-guide, mudar de convenção lint, arrumar indentações, remover espaços em brancos, remover comentários, etc..
fix: utilizado quando há correção de erros que estão gerando bugs no sistema.
Exemplo: Aplicar tratativa para uma função que não está tendo o comportamento esperado e retornando erro.
chore: indica mudanças no projeto que não afetem o sistema ou arquivos de testes. São mudanças de desenvolvimento.
Exemplo: Mudar regras do eslint, adicionar prettier, adicionar mais extensões de arquivos ao .gitignore
docs: usado quando há mudanças na documentação do projeto.
Exemplo: adicionar informações na documentação da API, mudar o README, etc.
build: utilizada para indicar mudanças que afetam o processo de build do projeto ou dependências externas.
Exemplo: Gulp, adicionar/remover dependências do npm, etc.
perf: indica uma alteração que melhorou a performance do sistema.
Exemplo: alterar ForEach por while, melhorar a query ao banco, etc.
ci: utilizada para mudanças nos arquivos de configuração de CI.
Exemplo: Circle, Travis, BrowserStack, etc.
revert: indica a reverão de um commit anterior.
Scope: contextualizando o commit
Nesse ponto — e seguindo as convenções passadas — conseguimos entender o tipo de alteração que foi realizada no commit (commit type) e entender com clareza o que o commit irá trazer se aplicado (commit subject).

Entretanto, até aonde essa mudança pode afetar ?

Em repositórios enormes, como monorepos, ou projetos com várias features e mudanças paralelas, não fica bastante claro até onde a mudança que irá chegar pode alterar. Para isso, podemos utilizar o escopo(scope) do commit.


Exemplo de commit utilizando o scope
Mesmo o scope não sendo obrigatório, ele pode ser utilizado para contextualizar o commit e trazer menos responsabilidade para a subject, uma vez que dispondo do tipo de commit e o contexto que foi aplicado, a mensagem deve ser o mais breve e concisa possível. Lembrando que o scope deve ser inserido no commit entre parênteses.

Além disso, no caso do scope é possível adicionarmos múltiplos valores, como por exemplo: Caso houvesse uma refatoração de código em um repositório com versões mobile, web e desktop. A qual afeta o contexto mobile e web, poderíamos escrever o commit da seguinte maneira:


Dessa maneira indicamos que é um commit de refatoração que afetara os contextos mobile e web da aplicação
Observação: Os escopos devem ser separados com / , \ ou ,.

https://arunkumarvallal.medium.com/become-a-pro-at-commit-messages-using-commitlint-56dab86333b3#:~:text=Commitlint%20maintains%20consistent%20formatting%20and,commit%20history%20and%20generate%20changelogs.