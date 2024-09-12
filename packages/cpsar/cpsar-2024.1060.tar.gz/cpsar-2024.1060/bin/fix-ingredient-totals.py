from __future__ import division
from __future__ import print_function
from builtins import str
from past.utils import old_div
import itertools
import sys

import cpsar.runtime as R
import cpsar.shell
import cpsar.util as U

#TODO get datetime.now as default end date and date - 30 for default start date

class Program(cpsar.shell.Command):

    def setup_options(self):
        super(Program, self).setup_options()
        self.add_option('-t', '--trans_ids', action="store_true", 
                dest="trans_ids", default=None, help='Tuple of trans_ids')
        self.add_option('-s', '--start_date', action="store_true", 
                default='20150717',
                help='Date to start searching for records')
        self.add_option('-e', '--end_date', action="store_true", 
                default='20150823',
                help='Date to stop searching for records')
        self.add_option('-g', '--group_numbers', action="store_true", 
                default=None,
                help='Touple of groups to override the default')

    def main(self):
        self._args = self._query_args()
        self._recalucated_ingredients = self._recalculate_ingredient_cost()
        self._update_ingredient_cost()

    @property
    def _groups_that_itemize(self):
        return ('70516', '70525', '70552', '70591', '70612')

    @property
    def _default_start_date(self):
        return self.opts.start_date 

    @property
    def _default_end_date(self):
        return self.opts.end_date 

    def _query_args(self):
        start_date = self._default_start_date
        end_date = self._default_end_date
        args = {
                'groups': self._groups_that_itemize,
                'start_date': start_date,
                'end_date': end_date
                }
        return args

    def ingredient_grouper(self, item):
        return item[0]

    @U.imemoize
    def _records(self):
        if self._trans_ids == ():
            print("There are no records to recalculate.")
            sys.exit()

        trans = self._get_trans_totals()
        all_ingredients = self._get_ingredients()
        all_ingredients.sort(key=self.ingredient_grouper)
        
        hist_ingredient_map = dict()
        for x, y in itertools.groupby(all_ingredients, self.ingredient_grouper):
            hist_ingredient_map[x] = list(y)

        data_recs = {}
        for trans_id, history_id, trans_total in trans: 
            ingredients = hist_ingredient_map[history_id]
            data_recs[trans_id] = {
                    'total': trans_total,
                    'history_id': history_id,
                    'ingredients': ingredients
                    } 
        return data_recs

    def _get_ingredients(self):
        cursor = R.db.cursor()
        cursor.execute("""
            SELECT
                h.history_id,
                h.ingredient_id,
                h.awp
            FROM trans as t
            LEFT JOIN history_ingredient as h USING(history_id)
            WHERE trans_id in %s 
            ORDER BY h.ingredient_id
        """ % (self._trans_ids,))
        return cursor.fetchall()

    def _get_trans_totals(self):
        cursor = R.db.cursor()
        cursor.execute("""
            SELECT
                trans_id,
                history_id,
                total
            FROM trans
            WHERE trans_id in %s 
        """% (self._trans_ids,))
        return cursor.fetchall()

    @property
    @U.imemoize
    def _trans_ids(self):
        if self.opts.trans_ids:
            return self.opts.trans_ids

        cursor = R.db.cursor()
        cursor.execute("""
            WITH ids AS (
            SELECT
                t.trans_id,
                h.history_id
            FROM history_ingredient AS h
            LEFT JOIN trans AS t USING(history_id)
            WHERE create_date BETWEEN '%(start_date)s' AND '%(end_date)s' 
                AND group_number in %(groups)s 
            GROUP BY trans_id, history_id
            ), ingredient_cost_sum AS (
            SELECT
                history_id,
                sum(cost) as cost
            FROM history_ingredient
            GROUP BY history_id
            ), record_data AS (
            SELECT 
                ids.trans_id,
                c.cost,
                trans.total
            FROM ids
            LEFT JOIN ingredient_cost_sum as c USING(history_id)
            LEFT JOIN trans USING (history_id)
            )
            SELECT 
                trans_id 
            FROM record_data
            WHERE cost != total
                    """ % (self._args))
        return tuple([str(i) for i, in cursor])

    def _recalculate_ingredient_cost(self):
        recalculated_costs = []
        for hist in self._fixed_ingredients():
            trans_total = hist['trans_total']
            ingredients = hist['ingredients']
            sum_of_costs_before_adj = sum(i['cost'] for i in ingredients)
            adjustment = trans_total - sum_of_costs_before_adj
            ingredients[0]['cost'] = ingredients[0]['cost'] + adjustment
            recalculated_costs.append({
                })

            # return or save this to the instance

    @U.imemoize
    def _fixed_ingredients(self):
        recs = self._records()
        fi = []

        for trans_id in recs:
            trans_data = recs[trans_id]
            ingredients = trans_data['ingredients']
            total_awp = sum(
                    [awp for history_id, ingredient_id, awp in ingredients])

            fingredients = [] 
            for history_id, ingredient_id, awp in ingredients:
                cost_ratio = old_div(awp, total_awp)
                money = U.count_money(cost_ratio * trans_data['total'])
                ingredient = {
                    'ingredient_id': ingredient_id,
                    'cost': money
                    }
                fingredients.append(ingredient)
            fi.append({
                'history_id': history_id,
                'trans_total': trans_data['total'],
                'ingredients': fingredients})
        return fi

    def _update_ingredient_cost(self):
        cursor = R.db.cursor()
        debug_list = []
        for hist in self._fixed_ingredients():
            ingredients = hist['ingredients']

            sum_costs = sum(ingredients['cost'] for ingredients in ingredients)
            debug_list.append({
                'history_id': hist['history_id'] , 
                'sum_costs': sum_costs})

            for ingredient in ingredients:
                ingredient_id = ingredient['ingredient_id']
                ingredient_cost = ingredient['cost']
                cursor.execute("""
                    UPDATE history_ingredient
                    SET cost = %s 
                    WHERE ingredient_id = '%s'
                """ % (ingredient_cost, ingredient_id))
        R.db.commit()

if __name__ == '__main__':
    Program().run()
