describe('Todo Test', function() {
    it('adds first Todo', function() {
      cy.visit('http://localhost:8080')
      cy.get("#add").click()
      cy.contains("new todo")
    })
    it('changes first name', function() {
        cy.visit('http://localhost:8080')
        cy.get("h1").first().click().type("{selectall}").type("na Servas").click()
        cy.contains("na Servas")
    })
    it('adds second Todo', function() {
        cy.visit('http://localhost:8080')
        cy.get("#add").click()
        cy.contains("new todo")
    })
    it('changes second name', function() {
        cy.visit('http://localhost:8080')
        cy.get("h1").last().click().type("{selectall}").type("jo mei")
        cy.contains("jo mei")
    })
    it('locks second', function() {
        cy.visit('http://localhost:8080')
        cy.get("[alt='lock']").last().click()
        cy.get("h1").last().click().type("{selectall}").type("herst oida")

        cy.once('fail', (err) => {
            expect(err.message).to.include('cy.type() failed because it requires a valid typeable element.');
        });

        cy.contains("jo mei")
    })
    it('unlocks second', function() {
        cy.visit('http://localhost:8080')
        cy.get("[alt='lock']").last().click()
        cy.get("h1").last().click().type("{selectall}").type("jo ferdl")
        cy.contains("jo ferdl")
    })
    it('deletes second', function() {
        cy.visit('http://localhost:8080')
        cy.get('[alt="delete"]').last().click()
    })
    it('adds subtodo', function() {
        cy.visit('http://localhost:8080')
        cy.get('.add').last().click()
    })
    it('rename subtodo', function() {
        cy.visit('http://localhost:8080')
        cy.get('h1').last().click().type("{selectall}").type("Grias enk")
    })
    it('locks first', function() {
        cy.visit('http://localhost:8080')
        cy.get("[alt='lock']").first().click()
        cy.get("h1").last().click().type("{selectall}").type("herst oida")

        cy.once('fail', (err) => {
            expect(err.message).to.include('cy.type() failed because it requires a valid typeable element.');
        });

        cy.contains("na Servas")
    })
    it('checks lock subtodo', function() {
        cy.visit('http://localhost:8080')
        cy.get("h1").last().click().type("{selectall}").type("herst oida")

        cy.once('fail', (err) => {
            expect(err.message).to.include('cy.type() failed because it requires a valid typeable element.');
        });

        cy.contains("Grias enk")
    })
    it('unlocks todo', function() {
        cy.visit('http://localhost:8080')
        cy.get("[alt='lock']").first().click()
    })
    it('deletes all', function() {
        cy.visit('http://localhost:8080')
        cy.get('[alt="delete"]').click({multiple:true,force:true})
    })
  })