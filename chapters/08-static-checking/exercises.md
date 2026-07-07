# Chapter 8 — Exercises

Exercises are graded by depth: **[warm‑up]** checks understanding, **[analysis]** asks you to
reason.

## Concepts

1. **[warm‑up]** In one or two sentences each, explain what makes a technique *static* rather
   than *dynamic*, and give one example of each from this book. Then state the single biggest
   thing static checking *cannot* tell you that testing (Chapter 9) can.

2. **[warm‑up]** Name the six phases of a traditional inspection in order, and give a
   one‑sentence purpose for each. Which phase finds most of the defects, and why is it *not*
   the meeting?

3. **[warm‑up]** List the five inspection roles (author, reviewer, reader, moderator, scribe)
   and, for each, state the one thing the inspection breaks down without. Explain why the
   author must never also be the moderator or reader of their own code.

4. **[warm‑up]** Define *false positive* and *false negative* for a static analyzer in your
   own words, and give a concrete one‑line example of each. Which one gives you *false
   reassurance*, and why is that the more dangerous error?

5. **[warm‑up]** Distinguish a *discovery* review from a *deep‑dive* review from a
   *retrospective* review by when each happens and what question it answers.

## Analysis

6. **[analysis]** A teammate proposes replacing your team's code reviews entirely with an
   aggressive static analyzer, arguing "the tool never gets tired and never misses a null
   check." Using the ideas of *intent*, *trust*, and *false negatives*, write a ~150‑word
   response explaining what the tool would catch, what it would miss, and why review and
   analysis are complementary rather than substitutes.

7. **[analysis]** Your team's static analyzer has 95% recall but a 55% false‑positive rate;
   developers have started dismissing its warnings without reading them. Explain, using
   precision/recall, why the *high recall* is now worthless in practice, and describe two
   concrete changes you would make to restore the team's trust in the tool. Would you accept
   *lower recall* to get there? Justify it.

8. **[analysis]** Fill in and interpret this confusion matrix. A checker was run on a module
   known (from later production incidents plus a hand audit) to contain 20 real defects of the
   kind the checker targets. The checker raised 30 alarms; 12 of them corresponded to real
   defects. Compute the true positives, false positives, and false negatives, then compute the
   tool's precision and recall. In one sentence, say whether you'd trust this tool and why.

9. **[analysis]** **Perform a code review.** Read the function below — the defects are real,
   and you can point a linter or type checker at it as well as your own eyes. List every defect
   and concern you would raise as a reviewer, and for each, label
   whether it is about *correctness*, *intent/design*, or *style/clarity*. Then state which
   one or two of these an ordinary automated linter or type checker would likely have caught on
   its own, and which require a *human* reviewer who understands intent.

   ```generic
   // Applies a discount code to a shopping cart and returns the new total.
   function applyDiscount(cart, code)
     total <- 0
     for each item in cart.items
       total <- total + item.price * item.quantity
     end for
     discount <- lookup code in discounts     // returns nothing if code is unknown
     total <- total - total * discount.percent / 100
     if total < 0 then
       total = 0
     end if
     cart.total <- total
     return total
   end function
   ```

   ```go
   // Applies a discount code to a shopping cart and returns the new total.
   func applyDiscount(cart *Cart, code string) float64 {
   	total := 0.0
   	for _, item := range cart.Items {
   		total = total + item.Price*float64(item.Quantity)
   	}
   	discount := discounts.Lookup(code) // returns nil if code is unknown
   	total = total - total*discount.Percent/100
   	if total < 0 {
   		math.Max(total, 0)
   	}
   	cart.Total = total
   	return total
   }
   ```

   ```java
   // Applies a discount code to a shopping cart and returns the new total.
   static double applyDiscount(Cart cart, String code) {
     double total = 0;
     for (Item item : cart.items) {
       total = total + item.price * item.quantity;
     }
     Discount discount = discounts.lookup(code);  // returns null if code is unknown
     total = total - total * discount.percent / 100;
     if (total < 0) {
       Math.max(total, 0);
     }
     cart.total = total;
     return total;
   }
   ```

   ```javascript
   // Applies a discount code to a shopping cart and returns the new total.
   function applyDiscount(cart, code) {
     let total = 0;
     for (const item of cart.items) {
       total = total + item.price * item.quantity;
     }
     const discount = discounts.lookup(code);   // returns null if code is unknown
     total = total - total * discount.percent / 100;
     if (total < 0) {
       total == 0;
     }
     cart.total = total;
     return total;
   }
   ```

   ```python
   # Applies a discount code to a shopping cart and returns the new total.
   def apply_discount(cart, code):
     total = 0
     for item in cart.items:
       total = total + item.price * item.quantity
     discount = discounts.lookup(code)        # returns None if code is unknown
     total = total - total * discount.percent / 100
     if total < 0:
       total == 0
     cart.total = total
     return total
   ```

   ```ruby
   # Applies a discount code to a shopping cart and returns the new total.
   def apply_discount(cart, code)
     total = 0
     cart.items.each do |item|
       total = total + item.price * item.quantity
     end
     discount = DISCOUNTS.lookup(code)        # returns nil if code is unknown
     total = total - total * discount.percent / 100
     if total < 0
       total == 0
     end
     cart.total = total
     total
   end
   ```

   ```typescript
   // Applies a discount code to a shopping cart and returns the new total.
   interface Item { price: number; quantity: number; }
   interface Cart { items: Item[]; total: number; }
   interface Discount { percent: number; }

   declare const discounts: { lookup(code: string): Discount | null };

   function applyDiscount(cart: Cart, code: string): number {
     let total = 0;
     for (const item of cart.items) {
       total = total + item.price * item.quantity;
     }
     const discount = discounts.lookup(code);   // returns null if code is unknown
     total = total - total * discount.percent / 100;
     if (total < 0) {
       total == 0;
     }
     cart.total = total;
     return total;
   }
   ```

10. **[analysis]** In an inspection meeting, a reviewer starts sketching, on the whiteboard, a
    better algorithm to replace the one under inspection, and a fifteen‑minute design debate
    breaks out. As the moderator, what rule is being violated, what do you say, and where does
    that redesign work properly belong? Explain *why* the meeting protects this boundary.

11. **[analysis]** The §8.2.2 case study found that raising the preparation rate above ~1,000
    lines/hour cut defect yield from ~8 to ~2 per thousand lines. A manager reads this as "great
    news — the faster reviews find fewer problems, so the code must be getting cleaner." Explain
    why this interpretation is exactly backwards, and describe the one metric you would add to
    the team's dashboard to expose the real story.
