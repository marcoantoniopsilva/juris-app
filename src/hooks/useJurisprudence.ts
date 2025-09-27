import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { supabase } from '@/integrations/supabase/client';

export const useJurisprudence = (searchParams: any) => {
  return useQuery({
    queryKey: ['jurisprudence', searchParams],
    queryFn: async () => {
      let query = supabase
        .from('jurisprudence')
        .select('*')
        .order('data', { ascending: false });
      
      if (searchParams.tribunal) {
        query = query.eq('tribunal', searchParams.tribunal);
      }
      
      if (searchParams.processo) {
        query = query.ilike('processo', `%${searchParams.processo}%`);
      }
      
      if (searchParams.relator) {
        query = query.ilike('relator', `%${searchParams.relator}%`);
      }
      
      const { data, error } = await query;
      
      if (error) throw error;
      return data;
    },
  });
};

export const useCreateJurisprudence = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: async (jurisData: any) => {
      const { data, error } = await supabase
        .from('jurisprudence')
        .insert(jurisData)
        .select()
        .single();
      
      if (error) throw error;
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['jurisprudence'] });
    },
  });
};